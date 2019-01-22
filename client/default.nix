with import <nixpkgs> {};

let

opencv3WithGtk = python36Packages.opencv3.override {
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
    python36
    python36Packages.numpy
    opencv3WithGtk
  ];

  shellHook = ''
  '';
}
