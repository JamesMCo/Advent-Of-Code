# https://stackoverflow.com/a/63792201
# Register a new tag, raw_include_relative, that wraps the returned data from include_relative in a raw tag
# (needed as some solution files, e.g. 2017/09/Part1.py, include liquid syntax errors - we don't want to render them with liquid at all!)
module Jekyll
    module Tags
        class RawIncludeRelativeTag < IncludeRelativeTag
            def read_file(file, context)
                "{% raw %}" + super + "{% endraw %}"
            end
        end
    end
end

Liquid::Template.register_tag("raw_include_relative", Jekyll::Tags::RawIncludeRelativeTag)