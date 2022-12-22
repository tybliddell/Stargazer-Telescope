# External Imports
from base64 import b64encode
import json
from queue import Queue
import uuid
import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from typing import Optional
from datetime import datetime
from threading import Thread, Lock
from config import EXPOSURES, GPS
from redis import Redis

# Internal Imports
from rhodesmill_skyfield.named_stars import NAMED_STARS


# This should change as we add more options to the star list
STAR_LIST_NAME = 'named_stars'


def send(response: str, connection: socket) -> None:
    try:
        connection.send((response + '\r\n\r\n').encode())
    except:
        pass
    return


def build_response(request_type: str, object_type: str, current_queue: list = None, finished_queue: list = None,
                   current_query: str = None, stars: list = None, star: dict = None, client_id: str = None, image: str = None) -> str:
    response = {key: val for key, val in locals().items() if val is not None}
    response['timestamp'] = str(datetime.now())
    return json.dumps(response)


class Request:

    def __init__(self, json_data: dict) -> None:
        # Should be in every request
        self.request_type = json_data.get('request_type')
        self.object_type = json_data.get('object_type')
        self.timestamp = json_data.get('timestamp')

        # In client_id request
        self.client_id = json_data.get('client_id')

        # Should be in all autonomous_queue requests
        self.current_queue = json_data.get('current_queue')
        self.current_queue_object = json_data.get('current_queue_object')
        self.finished_queue = json_data.get('finished_queue')

        # Should be in favorite_star_list or star_list requests
        self.stars = json_data.get('stars')
        self.star = json_data.get('star')
        self.current_query = json_data.get('current_query')

        self.finished_id = json_data.get('finished_id')

        self.stringified = str(json_data)
        return

    def is_valid(self) -> bool:
        return self.request_type and self.object_type and self.timestamp

    def is_connection_control(self) -> bool:
        return self.object_type == 'favorite_star_list'

    def __str__(self) -> str:
        return self.stringified


def is_json(message: str) -> Optional[dict]:
    try:
        return json.loads(message)
    except ValueError:
        return None


class ClientConnection:

    def __init__(self, connection: socket) -> None:
        self.connection = connection
        self.buffer_size = 8192
        self.favorites_list = []  # Looks like [{'dict': 'dict_name', 'object_name': 'name_here', 'object_info': 'object info'},]
        self.client_id = ''
        return

    def receive_data(self) -> Optional[Request]:
        try:
            data = self.connection.recv(self.buffer_size).decode()
            while '\r\n\r\n' not in data:
                if not (chunk := self.connection.recv(self.buffer_size).decode()):
                    return None
                data += chunk
            if (json_data := is_json(data)) is None:
                return None
            request = Request(json_data)
            if not request.is_valid():
                return None
            if not request.is_connection_control():
                return request
            self.process_request(request)
            return request
        except Exception as e:
            print(f"[server-exception] {e}")
            return None

    def process_request(self, request: Request) -> None:
        match request.request_type:
            case 'GET':
                send(build_response(request_type='SET', object_type='favorite_star_list', stars=self.favorites_list), self.connection)
            case 'ADD':
                if request.star not in self.favorites_list:
                    self.favorites_list.append(request.star)
            case 'REMOVE':
                if request.star in self.favorites_list:
                    self.favorites_list.remove(request.star)
        return

    def close_client(self) -> None:
        self.connection.close()
        self.connection = None
        print('[server-connection] connection closed')
        return


class Server:

    def __init__(self, in_queue: Queue, out_queue: Queue, exposure_time_left: dict, exposure_time_lock: Lock,  gps: GPS, address: str = None, port: int = None) -> None:
        self.address = address if address else '0.0.0.0'
        self.port = port if port else 2100
        
        # In and out queues for server (this thread)
        self.in_queue = in_queue
        self.out_queue = out_queue

        # Misc
        self.exposure_time_left = exposure_time_left
        self.exposure_time_lock = exposure_time_lock
        self.red = Redis(host='redis')
        self.sub = self.red.pubsub()
        self.gps = gps
        self.viewable_stars = {key: val for key, val in NAMED_STARS.items() if 90 > val['dec'] > 90 - gps.latitude}

        # Init variables
        self.threads: list[Thread] = []
        self.current_queue: list[dict] = []
        self.finished_queue: list[dict] = []
        self.pending_queue: list[dict] = []
        self.client_list: list[ClientConnection] = []
        # TODO: When you implement clearing finished queue, remove all those ids from this list
        self.used_ids: list[uuid.uuid1] = []

        # Set up thread for outbound queue
        Thread(target=self.handle_queues).start()

        # Set up listening socket
        self.listener = socket(AF_INET, SOCK_STREAM)
        self.listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.listener.bind((self.address, self.port))
        self.listener.listen()
        return

    # Populates out queue every 10 seconds
    # Run in a seperate thread 
    def handle_queues(self):
        while True:
            # out_queue going to alpaca client
            if self.out_queue.empty() and len(self.current_queue) > 0:
                next_star = self.current_queue.pop(0)
                self.pending_queue.append(next_star)
                self.out_queue.put(next_star)
                
            # in_queue coming from image processing thread
            while not self.in_queue.empty():
                star = self.in_queue.get()
                for s in self.pending_queue:
                    if s['star_id'] == star['star_id']:
                        break
                self.pending_queue.remove(star)
                self.finished_queue.append(star)
            time.sleep(5)

    # Continuously listen for connections
    # Spawns new thread to handle each connection
    def listen(self):
        print('[server-status] Listening for connections')
        while True:
            client_socket, _ = self.listener.accept()
            thread = Thread(target=self.accept_client, args=(client_socket,))
            self.threads.append(thread)
            thread.start()
            for thread in self.threads:
                if not thread.is_alive():
                    thread.join()
                    self.threads.remove(thread)
    
    def get_unique_id(self):
        client_id = str(uuid.uuid1())
        if client_id not in self.used_ids:
            self.used_ids.append(client_id)
            return client_id
        return self.get_unique_id()

    # Ensure client begins with INIT.
    # Gets client_id if used previously, otherwise create new id.
    # Continuously receive data from client and process it.
    # Returns when client disconnects or error occurs
    def accept_client(self, client_socket: socket) -> None:
        new_client = ClientConnection(client_socket)
        request = new_client.receive_data()
        if request is None:
            return
        if request.request_type != 'INIT':
            client_socket.close()
            print('[server-clienterror] client did not send INIT, closing connection')
            return
        # if client did not send id or sent id is not present in current client_list
        if not request.client_id or not len(clients := [client for client in self.client_list if client.client_id == request.client_id]):
            new_client.client_id = self.get_unique_id()
            send(build_response(request_type='INIT', object_type='client_id', client_id=new_client.client_id), client_socket)
            self.client_list.append(new_client)
            client = new_client
            print(f'[server-connection] client has connected with new id: {client.client_id}')
        else:
            client = clients[0]
            client.connection = client_socket
            print(f'[server-connection] client has connected with existing id: {client.client_id}')
        while (request := client.receive_data()) is not None:
            self.process_request(request, client)
        client.close_client()
        return

    def process_request(self, request: Request, client: ClientConnection) -> None:
        print(f'[server-message] {str(request)}')
        match request.request_type:
            case 'GET':
                self.handle_get(request, client)
            case 'SET':
                self.handle_set(request)
        return

    def handle_get(self, request: Request, client: ClientConnection) -> None:
        match request.object_type:
            case 'autonomous_queue':
                self.update_current_queue()
                send(build_response(request_type='SET', object_type='autonomous_queue', current_queue=self.current_queue, finished_queue=self.finished_queue), client.connection)
            case 'star_list':
                star_list = []
                for name, star in self.viewable_stars.items():
                    if str(name).lower().startswith(str(request.current_query).lower()):
                        star_list.append({
                            'dict': STAR_LIST_NAME,
                            'object_name': name,
                            'object_info': f"{name}'s IAU designation is {star['Designation']} and is part of the {star['Constellation']} constellation."
                        })
                send(build_response(request_type='SET', object_type='star_list', stars=star_list), client.connection)
            case 'processed_image':
                if (image := self.get_image_from_db(request.finished_id)) is not None:
                    temp = b64encode(image)
                    send(build_response(request_type='SET', object_type='processed_image', image=temp.decode()), client.connection)
        return
    
    def handle_set(self, request: Request) -> None:
        match request.object_type:
            case 'autonomous_queue':
                temp_queue = [{'star_id': self.get_unique_id()} | star for star in request.current_queue if not self.is_pending(star)]
                # expand each entry in temp_queue
                self.current_queue = temp_queue
        return
    
    def update_current_queue(self) -> None:
        with self.exposure_time_lock:
            time_to_start = [self.exposure_time_left['seconds']]
        for star in self.current_queue:
            star['time_to_start'] = sum(time_to_start)
            time_to_start.append(sum(EXPOSURES[star['image_quality']]))
    
    def is_pending(self, star) -> bool:
        return star.get('star_id') in [temp['star_id'] for temp in self.pending_queue if 'star_id' in temp]

    def get_image_from_db(self, db_id):
        if db_id is None:
            print('[server-message] received null id')
            return None
        image = self.red.get(db_id)
        return image
