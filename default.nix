{ pkgs ? import <nixpkgs> { } }:

with pkgs.python310Packages;

buildPythonApplication {
  pname = "aboutlife";
  version = "0.0.1";
  format = "pyproject";

  # TODO: fetch from repo
  src = ./.;

  nativeBuildInputs = [
    pkgs.wrapGAppsHook
    pkgs.gobject-introspection
    pkgs.python310Packages.hatchling
  ];

  buildInputs = [
    pkgs.gtk3
    pkgs.vte
    pkgs.python310
  ];

  propagatedBuildInputs = [
    pkgs.python310Packages.pygobject3
    pkgs.python310Packages.xlib
  ];

  doCheck = false;

  meta = {
    description = "Computer usage regulation tool";
    mainProgram = "aboutlife";
  };
}
