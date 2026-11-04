#version 150 core

in vec4 vertex_colors;
out vec4 fragColor;  // ← Must be fragColor

void main()
{
    fragColor = vertex_colors;
    
    if (fragColor.a < 0.01) {
        discard;
    }
}
