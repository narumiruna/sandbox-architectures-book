pi:
    pi -ne \
        -e https://github.com/cathrynlavery/diagram-design \
        -e npm:@narumitw/pi-subagents \
        -e npm:@narumitw/pi-goal

serve:
    uv run --locked zensical serve
