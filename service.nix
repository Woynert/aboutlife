{ config, lib, pkgs, ... }:
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

      startLimitIntervalSec = 350;
      startLimitBurst = 10;
      serviceConfig = {
        # use user environment and packages
        ExecStart = "${pkgs.bash}/bin/bash -c 'source ${config.system.build.setEnvironment}; exec ${aboutlife}/bin/aboutlife --obfuscated'";
        # do not kill spawned processes on stop
        KillMode = "process"; 
        Restart = "always";
        RestartSec = 60;
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
