{ config, lib, ... }:
with lib;
let
  cfg = config.services.aboutlife;
  aboutlife = (import ./default.nix { });

in
{
  options.services.aboutlife = {
    enable = mkEnableOption "Enable aboutlife service";
    greeter = mkOption {
      type = types.bool;
      default = false;
    };
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
        Restart = "always";
        RestartSec = 3;
      };
    };

    systemd.user.timers.aboutlife = {
      description = "Ensure aboutlife is running";
      wantedBy = [ "timers.target" ];
      timerConfig = {
        OnCalendar = "*-*-* *:0:00"; # every hour
        Persistent = true;
      };
    };
  };
}
