with import <nixpkgs> {};

let

python = python37;
pythonPackages = python37Packages;

opencv3WithGtk = pythonPackages.opencv3.override {
  enableGtk3 = true;
  enableFfmpeg = true;
};

pyrr = with pkgs; callPackage ./pyrr.nix {
    inherit (pythonPackages)
      buildPythonPackage
      fetchPypi
      setuptools
      multipledispatch
      numpy;
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
    pyrr
    ] ++ (with pythonPackages; [
      numpy
      pillow
      pyqt5
      moderngl
    ]);
}
