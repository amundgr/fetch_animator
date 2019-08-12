import numpy as np 
import copy as cp

frame_1 = np.array([
            [  1,  0,  0,  0,  0,  0,  0,  0, 10, 11,  0,  0,  0,  0,  0,  0,  0, 11,  1],
            [  1,  8,  0,  0,  0,  0,  0,  8,  0,  0,  9,  0,  0,  0,  0,  0,  9,  0,  2],
            [  1,  0,  6,  0,  0,  0,  6,  0,  0,  0,  0,  7,  0,  0,  0,  7,  0,  0,  3],
            [  1,  0,  0,  4,  0,  4,  0,  0,  0,  0,  0,  0,  5,  0,  5,  0,  0,  0,  4],
            [  1,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  5],
            [  1,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  6],
            [  1,  0,  0,  4,  0,  4,  0,  0,  0,  0,  0,  0,  5,  0,  5,  0,  0,  0,  7],
            [  1,  0,  6,  0,  0,  0,  6,  0,  0,  0,  0,  7,  0,  0,  0,  7,  0,  0,  8],
            [  1,  8,  0,  0,  0,  0,  0,  8,  0,  0,  9,  0,  0,  0,  0,  0,  9,  0,  9],
            [  1,  0,  0,  0,  0,  0,  0,  0, 10, 11,  0,  0,  0,  0,  0,  0,  0, 11, 10]])

frames = [frame_1]            
pwm_frames = []
with open("out.bin", "wb") as fp:
    for f in frames:
        frame = cp.deepcopy(f)
        frame = np.flip(frame, 0)
        len_y, len_x = frame.shape
        binary_factors = 2**np.linspace(0,len_y, len_y+1)[0:-1]

        binary_frame_matrix = (frame > 0)
        binary_frame_array = np.sum(binary_frame_matrix * binary_factors.reshape(-1,1), 0)
        binary_frame_array_uint32 = np.uint32(binary_frame_array.astype(int))

        frame[frame == 0] = 20
        pwm_frame_uint8 = np.uint8(frame)
        
        fp.write(bytes(binary_frame_array_uint32))
        pwm_frames.append(pwm_frame_uint8)

    for pwm_frame in pwm_frames:
        fp.write(bytes(pwm_frame))
