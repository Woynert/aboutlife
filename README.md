# Aboutlife

Build nix derivation:

```sh
nix-build default.nix
```

Run from nix-shell:

```sh
nix-shell -p 'import (./default.nix) {}' --run aboutlife
```

Run from git:

```sh
nix-shell -p 'import (fetchFromGitHub { owner="woynert";repo="aboutlife";rev="master";sha256="sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"; }) {}' --run aboutlife
```

*Flake: coming soon*

## License

Nature images: https://freenaturestock.com/license/

## Philosophy

Do not limit the user to the point they may want to disable the service "just for this one time", they will always find a way to disable it. 

Moreover, this tool should only make it easier for the user to recognize their bad patterns and to organize their time on the computer.
