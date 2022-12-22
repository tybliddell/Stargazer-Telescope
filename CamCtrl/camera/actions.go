package camera

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"os/exec"
)

var gphoto string = "gphoto2"

type ICamera interface {
	Connect() bool
	Capture(float32, string)
	Cancel()
	gphoto(arg ...string) exec.Cmd
}

type Camera struct {
	ICamera
	ctx    context.Context
	cancel context.CancelFunc
}

type image struct {
	data []byte
	err  error
}

func (c *Camera) Cancel() {
	// if canceled we need to create a new context
	c.cancel()
	c.ctx, c.cancel = context.WithCancel(context.TODO())
}

// internal helper fn to call gphoto commands with the correct context
func (c *Camera) gphoto(arg ...string) exec.Cmd {
	return *exec.CommandContext(c.ctx, "gphoto2", arg...)
}

// Connect to the camera
func (c *Camera) Connect() error {
	c.ctx, c.cancel = context.WithCancel(context.TODO())
	cmd := c.gphoto("--auto-detect")
	cmd.Run()
	cmd = c.gphoto("--list-all-config")
	return cmd.Run()
}

//export Capture
func (c *Camera) Capture(def ImgDef) ([]byte, error) {
	var r io.Reader
	var w io.WriteCloser
	debug := false
	r, w = io.Pipe()
	imgch := make(chan image)
	// check for capture complete in a separate thread
	go func() {
		var buffer bytes.Buffer
		// block and download image
		if err := downloadImage(r, &buffer); err == nil {
			c.Cancel()
			imgch <- image{data: buffer.Bytes(), err: nil}
		} else {
			c.Cancel()
			imgch <- image{data: nil, err: err}
		}

	}()

	timeunit := fmt.Sprintf("%.2f%s", def.Time, def.Unit)
	// take a bulb capture for the specified time and wait two minutes for the image to download
	cmd := c.gphoto("--stdout", "--set-config", "bulb=1", "--wait-event", timeunit, "--set-config", "bulb=0", "--wait-event-and-download", "10s")
	
	if debug {
		w.Close()
		img := <-imgch
		return img.data, img.err
	}

	//blocks until image is ready

	cmd.Stdout = w
	cmd.Stderr = w
	
	if err := cmd.Run(); err != nil {
		w.Close()
		return nil, err
	}
	w.Close()
	img := <-imgch
	return img.data, img.err
}

func downloadImage(reader io.Reader, buffer *bytes.Buffer) error {
	// Every ARW image starts with this sequence of bytes
	preamble := []byte{0x49, 0x49, 0x2A, 0x00, 0x08, 0x00, 0x00, 0x00, 0x13, 0x00, 0xFE, 0x00, 0x04, 0x00, 0x01, 0x00}
	seeker := make([]byte, 1024)
	imgFound := false
	for {
		_, err := reader.Read(seeker)
		if err != nil && err != io.EOF {
			return err
		} else if err != nil {
			break
		}

		if !imgFound {
			_, img, found := bytes.Cut(seeker, preamble)
			if found {
				buffer.Write(preamble)
				buffer.Write(img)
				imgFound = true
			}
		} else {
			buffer.Write(seeker)
		}
	}

	return nil

}
