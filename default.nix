# default.nix
{ pkgs ? import <nixpkgs>{} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages (python-pkgs: with python-pkgs; [
      # select Python packages here
      torch
      torchvision
      torchaudio
      tensorboard
      torch-tb-profiler
      ipywidgets
      matplotlib
      plotly
      ipykernel
    ]))
    jupyter
    pipenv
    quarto
    graphviz
  ];
}
