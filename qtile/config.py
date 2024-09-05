from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from colors2 import *
import os
import subprocess

mod = "mod4"
terminal = "kitty"

# Autostart
@hook.subscribe.startup_once
def auto_start():
    global home
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# File to store the current theme index
theme_file = os.path.expanduser("~/.config/qtile/current_theme.txt")

# Function to read the current theme index from the file
def read_current_theme():
    try:
        with open(theme_file, "r") as f:
            index = int(f.read().strip())
            return index
    except:
        return 0

# Function to write the current theme index to the file
def write_current_theme(index):
    with open(theme_file, "w") as f:
        f.write(str(index))

# Initialize the current theme index
current_theme_index = read_current_theme()
current_colors = color_schemes[current_theme_index]

def update_wallpaper_and_colors(qtile, index):
    global current_colors, current_theme_index
    wallpaper = wallpapers[index]
    current_colors = color_schemes[index]
    current_theme_index = index
    write_current_theme(index)

    # Set the new wallpaper
    subprocess.run(["nitrogen", "--set-zoom-fill", wallpaper])
    subprocess.run(["wal", "-i", wallpaper])

    # Reload the Qtile configuration to apply the new colors
    qtile.cmd_reload_config()

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 1%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 1%+")),

    # Change wallpaper
    Key(["control", "mod1"], "1", lazy.function(update_wallpaper_and_colors, 0)),
    Key(["control", "mod1"], "2", lazy.function(update_wallpaper_and_colors, 1)),
    Key(["control", "mod1"], "3", lazy.function(update_wallpaper_and_colors, 2)),
    Key(["control", "mod1"], "4", lazy.function(update_wallpaper_and_colors, 3)),
    Key(["control", "mod1"], "5", lazy.function(update_wallpaper_and_colors, 4)),
    # Brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key(["control"], "2", lazy.spawn("xbacklight -dec 5")),
    Key(["control"], "1", lazy.spawn("xbacklight -inc 5")),

    # Custom
    Key([mod, "mod1"], "r", lazy.spawn("launcher.sh -show drun spotlight")),
    Key([mod, "mod1"], "f", lazy.spawn("firefox")),
    Key([mod, "mod1"], "d", lazy.spawn("discord")),
    Key([mod, "mod1"], "o", lazy.spawn("obsidian")), 
    Key([mod, "mod1"], "n", lazy.spawn("thunar")),
    Key(["mod1"], "s", lazy.spawn("gnome-screenshot -i")),
    Key([mod, "control"], "z", lazy.spawn(f"{terminal} -e bash -c 'nvim .config/qtile/config.py'")),
    Key([mod, "control"], "x", lazy.spawn(f"{terminal} -e bash -c 'nvim .config/qtile/autostart.sh'")),
    Key([mod, "control"], "c", lazy.spawn(f"{terminal} -e bash -c 'python3 .config/qtile/config.py'")),
    Key([mod, "control"], "a", lazy.spawn(f"{terminal} -e bash -c ani-cli")),
    Key([mod, "control"], "s", lazy.spawn("shutdown -h now")),
    Key([mod, "control"], "w", lazy.spawn("nitrogen")),
    Key([mod, "control"], "b", lazy.spawn("reboot")),
    Key([mod, "mod1"], "m", lazy.spawn("flatpak run info.febvre.Komikku")),

    # Toggle between split and unsplit sides of stack.
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

layout_theme = {
    "border_width": 0,
    "margin": 6,
    "border_focus": current_colors["1"],
    "border_normal": current_colors["2"]
}

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
            # mod + shift + group number = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Switch to & move focused window to group {}".format(i.name)),
        ]
    )

layouts = [    
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.RatioTile(**layout_theme),
]

widget_defaults = dict(
    font="SauceCodePro Nerd Font Mono",
    fontsize=13,
    padding=4,
    
    foreground=current_colors["5"]
)
extension_defaults = widget_defaults.copy()

# Define the bar and widgets
def init_widgets_list(colors):
    widgets_list = [
        widget.Image(
            filename="~/.config/qtile/icons/qtile-logo.png"),
        widget.CurrentLayout(padding=8),
        widget.GroupBox(
            active=colors["3"],
            inactive=colors["5"],
            this_current_screen_border=colors["4"],
            this_screen_border=colors["2"],
            other_current_screen_border=colors["2"],
            other_screen_border=colors["2"],
            highlight_method='line',
            highlight_color=colors["1"],
        ),
        widget.Prompt(),
        widget.WindowName(padding=0),
        widget.Spacer(),
        widget.LaunchBar(
            progs=[
                ("/home/m_j2oz/MyStuff/icons/kurumi.png", 'thunar'),
                ('/home/m_j2oz/MyStuff/icons/firefox.png', 'firefox'),
                ("/home/m_j2oz/MyStuff/icons/code.png", "code"),
                ("/home/m_j2oz/MyStuff/icons/Xreader.png", "xreader"),
                ("/home/m_j2oz/MyStuff/icons/komikku2.jpg", "flatpak run info.febvre.Komikku")
            ],
        ),
        widget.Spacer(),
        widget.Systray(),
        widget.Bluetooth(
                    hci="hci0",
                    default_text='BT',
                    adapter_format='Adapter: {name} [{powered}{discovery}]',
                    default_show_battery=True
                ),
        widget.Spacer(length=3),
        #widget.Volume(),
        widget.CPU(),
        widget.Spacer(length = 3),
        widget.Memory(format='Mem: {MemUsed:.0f}{mm}'),
        widget.Spacer(length= 3),
        widget.Battery(format="{percent:2.0%}"),
        widget.Spacer(length = 3),
        widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
    ]
    return widgets_list


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_list(current_colors),
                size=24,
                #opacity = 0.9,
                background="#00000000"   
            ),
            
        ),
    ]

screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(border_focus=current_colors["1"], border_width=2)
auto_fullscreen = False
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wmname = "LG3D"
