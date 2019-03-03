{ nixpkgs ? import <nixpkgs> {} }:

with nixpkgs;
with lib;

let

  python = python37;
  pythonPackages = python37Packages;

  pythonEnv = python.buildEnv.override {
    extraLibs = with pythonPackages; [
      # dev
      jedi
      autopep8
      # deps
      aiohttp
    ];
  };

in

mkShell {
  name = "led-table-server";

  buildInputs = [
    pythonEnv
  ];
}
