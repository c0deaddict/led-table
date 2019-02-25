with import <nixpkgs> {};

let

python = python37;
pythonPackages = python37Packages;

opencv3WithGtk = pythonPackages.opencv3.override {
  enableGtk3 = true;
  enableFfmpeg = true;
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
    ] ++ (with pythonPackages; [
      numpy
      pillow
      pyrr
      pyqt5
      moderngl
    ]);
}
