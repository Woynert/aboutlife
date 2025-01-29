{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  name = "dev-environment";
  buildInputs = [
    pkgs.git
    pkgs.zip
    pkgs.ruff # formatter
    pkgs.pyright # lsp

    pkgs.gtk3
    pkgs.vte
    pkgs.gobject-introspection
    pkgs.python310
    pkgs.python310Packages.pygobject3
    pkgs.python310Packages.xlib
    pkgs.python310Packages.hatchling
    pkgs.python310Packages.requests
    pkgs.python310Packages.setproctitle
    pkgs.python310Packages.psutil

    pkgs.corepack
    pkgs.nodejs-slim
  ];
  shellHook = ''
    echo "Starting development shell"

    # custom prompt
    if [ -e ~/.gitconfig ] && [ -f ~/.git-prompt.sh ]; then
      source ~/.git-prompt.sh
      PS1='\[\033[01;33m\]nix:\w\[\033[01;34m\]$(__git_ps1 " %s")\[\033[33m\]\$\[\033[00m\] '
    fi
  '';
}

