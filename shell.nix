# save this as shell.nix
{ pkgs ? import <nixpkgs> {}}:
let
  callPackage = path: overrides:
    let f = import path;
    in f ((builtins.intersectAttrs (builtins.functionArgs f) pkgs) // overrides);

  customPython = pkgs.python39.withPackages(ps: with ps; [
    flake8
    isort
    mypy
    pytest
    coveralls
    build
    twine
  ]);
in
  pkgs.mkShell {
    buildInputs = [ customPython ];
  }
