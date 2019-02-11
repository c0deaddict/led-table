with import <nixpkgs> {};

let

python = python37;
pythonPackages = python37Packages;

opencv3WithGtk = pythonPackages.opencv3.override {
  enableGtk3 = true;
  enableFfmpeg = true;
};

ModernGL = callPackage ./moderngl.nix {
  inherit (pythonPackages) buildPythonPackage fetchPypi;
};

in

stdenv.mkDerivation rec {
  name = "env";

  env = buildEnv { name = name; paths = buildInputs; };
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup; ln -s $env $out
  '';

  buildInputs = [
    python
    opencv3WithGtk
    ModernGL
    ] ++ (with pythonPackages; [
      numpy
      pillow
      pyrr
      pyqt5
    ]);
}
