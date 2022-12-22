package camera

import (
	"regexp"
	"strconv"
)

type ImgDef struct {
	Time float32
	Unit string
}

func (d ImgDef) New(def string) ImgDef {
	regx := regexp.MustCompile(`^(\d+)([msh])$`)
	matches := regx.FindAllStringSubmatch(def, -1)
	if len(matches) == 0 || len(matches[0]) < 3 {
		return d
	}

	t, err := strconv.ParseFloat(matches[0][1], 32)
	if err != nil {
		return d
	}

	d.Time = float32(t)
	d.Unit = matches[0][2]
	return d
}
