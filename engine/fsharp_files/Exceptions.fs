namespace Scrabble.Core
open System

exception InvalidMoveException of string
exception UnsupportedCoordinateException of string