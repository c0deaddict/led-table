{ stdenv
, buildPythonPackage
, fetchPypi
, libGL
, libX11
}:

buildPythonPackage rec {
  pname = "moderngl";
  version = "5.5.0";

  src = fetchPypi {
    inherit pname version;
    sha256 = "0x8xblc3zybp7jw9cscpm4r5pmmilj9l4yi1rkxyf0y80kchlxq4";
  };

  buildInputs = [ libGL libX11 ];
}
