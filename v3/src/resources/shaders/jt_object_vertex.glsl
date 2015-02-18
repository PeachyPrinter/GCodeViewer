#version 330 core

in vec4 vPosisition;
in vec4 vColor;

out vec4 color;

uniform mat4 vProjection;
uniform vec4 vTranslate;

void main(){
    gl_Position = vProjection * (vPosisition + vTranslate);
    color = vColor;
}