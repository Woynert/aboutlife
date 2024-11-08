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
    pkgs.networkmanager
  ];

  propagatedBuildInputs = [
    pkgs.python310Packages.pygobject3
    pkgs.python310Packages.xlib
    pkgs.python310Packages.requests
    pkgs.python310Packages.setproctitle
    pkgs.python310Packages.psutil
  ];

  doCheck = false;

  meta = {
    description = "Computer usage regulation tool";
    mainProgram = "aboutlife";
  };
}
