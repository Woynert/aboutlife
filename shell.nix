{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	name = "dev-environment";
	buildInputs = [
		pkgs.git
        pkgs.wrapGAppsHook
        pkgs.ruff

        pkgs.python310
        pkgs.python310Packages.pygobject3
        pkgs.python310Packages.xlib

        pkgs.vte
        pkgs.libgudev
        pkgs.pcre2
		pkgs.gtk3
        pkgs.gobject-introspection
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

