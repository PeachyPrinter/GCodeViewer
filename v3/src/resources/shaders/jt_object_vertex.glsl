#version 330 core

in vec4 vPosisition;
in vec4 vColor;

out vec4 color;

uniform mat4 vProjection;
uniform mat4 vCamera;

void main(){
    vec4 newColor;
    mat4 thisone = mat4( 
        1.0,    0.0,    0.0,    0.0,
        0.0,    1.0,    0.0,    0.0,
        0.0,    0.0,    1.0,    0.0,
       -0.1,    0.1,   -3.0,    1.0
        );

    vec4 b = vPosisition + vec4(-0.1, 0.1, -3.0, 0.0);
    vec4 c = thisone * vPosisition;

    if (vColor == vec4(0.0,0.0,0.0,0.0)){

    }

    if (abs(b.x - c.x) < 0.001){
        newColor = vec4(0.0,1.0,0.0,1.0);
    } else {
        newColor = vec4(abs(b.z - c.z),0.0,0.0,1.0);
    }

    gl_Position = vProjection * vCamera * vPosisition;
    color = vColor;
}