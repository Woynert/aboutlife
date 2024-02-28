{ config, lib, ... }:
with lib;
let
  cfg = config.services.aboutlife;
  aboutlife = (import ./default.nix { });

in
{
  options.services.aboutlife = {
    enable = mkEnableOption (lib.mdDoc "Enable aboutlife service");
  };

  config = mkIf cfg.enable {
    systemd.user.services.aboutlife = {
      description = "Computer usage regulation tool";
      wantedBy = [ "graphical-session.target" ];
      partOf = [ "graphical-session.target" ];

      path = config.environment.systemPackages;

      startLimitIntervalSec = 350;
      startLimitBurst = 10;
      serviceConfig = {
        ExecStart = "${aboutlife}/bin/aboutlife";
        Restart = "on-failure";
        RestartSec = 3;
      };
    };
  };
}
