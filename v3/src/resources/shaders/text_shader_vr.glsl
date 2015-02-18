#version 330 core

in vec2 vPosisition;
in vec4 vColor;
in vec2 vTexCoord;

out vec4 color;
out vec2 texCoord;

uniform vec2 vWindow;

void main(){
    mat4 projection = mat4 (  2.0 / vWindow.x,   0.0,               0.0,        0.0,
                              0.0,               2.0 / vWindow.y,   0.0,        0.0,
                              0.0,               0.0,              -2.0,        1.0,
                              0.0,               0.0,               0.0,        1.0  );

    gl_Position =  projection *  (vec4(vPosisition.x - (vWindow.x / 2.0), vPosisition.y - (vWindow.y / 2.0),0.0,1.0));
    color = vColor;
    texCoord = vTexCoord;
 }