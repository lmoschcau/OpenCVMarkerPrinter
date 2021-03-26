#!/usr/bin/env python3
from MarkerPrinter import *
import cairo
import cairosvg


def generateMultiple(filenameFormat, filenameBase, dictionary, firstID, count, extensions=[], markerSize=100, markerResolution=1024, borderBits=1, verbose=False):
  _firstID = int(firstID)
  _count = int(count)
  _markerSize = int(markerSize)
  _markerResolution = int(markerResolution)
  _borderBits = int(borderBits)

  _extensions = list()
  extension_functions = {
    "png": cairosvg.svg2png,
    "pdf": cairosvg.svg2pdf,
    "ps": cairosvg.svg2ps,
    "eps": cairosvg.svg2eps,
  }
  extension_units = {
    "png": "px",
    "pdf": "cm",
    "ps": "px",
    "eps": "px",
  }

  for ext in extension_functions:
    if ext in extensions:
      _extensions.append(ext)

  if verbose:
    print("[INFO] filename format:         " + filenameFormat)
    print("[INFO] filename base:           " + filenameBase)
    print("[INFO] dictionary:              " + dictionary)
    print("[INFO] first id:                " + str(_firstID))
    print("[INFO] count:                   " + str(_count))
    print("[INFO] converting to filetypes: " + str(_extensions))
    print("[INFO] marker size:             " + str(_markerSize))
    print("[INFO] marker resolution:       " + str(_markerResolution))
    print("[INFO] border bits:             " + str(_borderBits))

  for _id in range(_firstID, _firstID + _count):
    if verbose: print("[INFO] exporting marker {id}".format(id=_id))

    # export svg marker
    filenameSVG = filenameFormat.format(dictionary=dictionary, extension="svg", size=str(_markerSize) + "cm", basename=filenameBase, id=_id)
    MarkerPrinter.GenArucoMarkerImage(filenameSVG, dictionary, _id, _markerSize/100, borderBits=_borderBits, pageBorder=(0, 0))

    # convert into other file types
    for ext in _extensions:
      # get filename
      filenameExt = filenameFormat.format(dictionary=dictionary, extension=ext, size=(str(_markerResolution) if extension_units[ext] == "px" else str(_markerSize) ) + extension_units[ext], basename=filenameBase, id=_id)
      # if the directory does not exist create it first
      directory, nameExt = os.path.split(filenameExt)
      if not os.path.exists(directory):
        os.makedirs(directory)
      
      # convert file
      extension_functions[ext](url=filenameSVG, write_to=filenameExt, output_width=_markerResolution, output_height=_markerResolution)



if __name__ == "__main__":

  parser = ArgumentParser()
  # Parameters
  # fileName
  parser.add_argument(
      "--filename_format", dest="filenameFormat", default="./{dictionary}/{extension}/{size}/{basename}{id:04d}.{extension}",
      help="Save marker image based on FORMAT. Available format strings: dictionary, extension, size, basename, id. 'size' is in cm for svg and px for png", metavar="FORMAT")
  parser.add_argument(
      "--filename_base", dest="filenameBase", default="aruco_",
      help="Basename for the filename_format", metavar="FORMAT")
  parser.add_argument(
      "--extensions", dest="extensions", default="png",
      help="Filetypes that should be generated as comma separated list", metavar="FORMAT")

  # dictionary
  parser.add_argument(
      "--dictionary", dest="dictionary", default="DICT_4X4_1000",
      help="Generate marker via predefined DICTIONARY aruco dictionary", metavar="DICTIONARY")

  # size
  parser.add_argument(
      "--marker_size", dest="markerSize", default="100",
      help="Save marker image with L marker size in x and y (Unit: cm)", metavar="L")
  parser.add_argument(
      "--marker_resolution", dest="markerResolution", default="1024",
      help="Save marker image with R marker resolution in x and y (Unit: pixel)", metavar="R")

  # else
  parser.add_argument(
      "--first_marker", dest="firstMarker", default="0",
      help="Save marker images that start with ID marker", metavar="ID")
  parser.add_argument(
      "--count", dest="count", default="10",
      help="Save C marker images", metavar="C")
  parser.add_argument(
      "--border_bits", dest="borderBits", default="1",
      help="Save marker image with N border size", metavar="N")

  # Run
  args = parser.parse_args()

  # split extension list
  extensions = args.extensions.replace(" ", "").split(",")

  generateMultiple(args.filenameFormat, args.filenameBase, args.dictionary, args.firstMarker, args.count, extensions, args.markerSize, args.markerResolution, args.borderBits, True)
