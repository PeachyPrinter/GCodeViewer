import numpy as np


def getLookAtMatrix(eye_point, look_at_point, up_vector):
    rotation_z = eye_point - look_at_point
    rotation_z = rotation_z / np.linalg.norm(rotation_z)

    rotation_x = np.cross(up_vector, rotation_z)
    rotation_x = rotation_x / np.linalg.norm(rotation_x)

    rotation_y = np.cross(rotation_z, rotation_x)
    rotation_y = rotation_y / np.linalg.norm(rotation_y)

    rotation_matrix = np.eye(4)
    rotation_matrix[0][0] = rotation_x[0]
    rotation_matrix[0][1] = rotation_x[1]
    rotation_matrix[0][2] = rotation_x[2]
    rotation_matrix[1][0] = rotation_y[0]
    rotation_matrix[1][1] = rotation_y[1]
    rotation_matrix[1][2] = rotation_y[2]
    rotation_matrix[2][0] = rotation_z[0]
    rotation_matrix[2][1] = rotation_z[1]
    rotation_matrix[2][2] = rotation_z[2]

    translation_matrix = np.eye(4)
    translation_matrix[0][3] = -eye_point[0]
    translation_matrix[1][3] = -eye_point[1]
    translation_matrix[2][3] = -eye_point[2]

    look_at_matrix = np.dot(rotation_matrix, translation_matrix).transpose()
    return look_at_matrix
