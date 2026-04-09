#{ pkgs ? import <nixpkgs> { } }: # Uncomment to use system derivation.
{ }:
let

# Use pinned Nixpkgs derivation (nixos-24.11.713895.666e1b3f09c2).
system = "x86_64-linux";
mkPinnedNixpkgs = { rev, sha256 }:
  import (builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
    inherit sha256;
  }) { inherit system; };
pkgs = mkPinnedNixpkgs {
  rev = "666e1b3f09c2";
  sha256 = "02cpqb4zdirzxfj210viim1lknpp0flvwcc1a2knmrmhl1f9dgz8";
};

in

with pkgs.python310Packages;

buildPythonApplication {
  pname = "aboutlife";
  version = "0.0.3";
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
