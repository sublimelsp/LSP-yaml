# LSP-yaml

YAML support for Sublime's LSP plugin. Basically a fork of [sublimelsp/LSP-json](https://github.com/sublimelsp/LSP-json).

Uses [yaml-language-server](https://github.com/redhat-developer/yaml-language-server) to provide validation, formatting and other features for YAML files. See linked repository for more information.

By default, schemas are automatically retrieved from [schemastore.org](http://schemastore.org/).

## Install

* Open the command palette and run `Package Control: Install Package`, then select [`LSP`](https://packagecontrol.io/packages/LSP)
* *~Install `LSP-yaml` from Package Control.~* Clone this repository into your Packages directory (`Preferences > Browse Packages...`). Open the command palette and run `Package Control: Satisfy Dependencies.`
* Restart Sublime.

## Configuration

Open configuration file using command palette with `Preferences: LSP-yaml Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-yaml`).

## Development

Clone this repository into your Packages directory. Open the command palette and run `Package Control: Satisfy Dependencies.`
