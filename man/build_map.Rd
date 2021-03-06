% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/build_map.R
\name{build_map}
\alias{build_map}
\title{Convert formatted rasters to minecraft worlds}
\usage{
build_map(lcm, dtm, name = gsub("^dtm-", "", gsub(".csv$", "",
  basename(dtm))), outDir = ".", verbose = FALSE)
}
\arguments{
\item{lcm}{Character, path to formatted lcm}

\item{dtm}{Character, path to formatted dtm}

\item{name}{Character, the name of the map, ususally the location. The name of the world is taken
from the input files by default.}

\item{outDir}{Character, the location the save the results, usually a temporary location}

\item{verbose}{Should python progress be printed. This is a bit buggy.}
}
\value{
Path to the minecraft map
}
\description{
This function uses a python script to convert the files produced by 
format_raster into minecraft maps. The name of the world is taken
from the input files
}
