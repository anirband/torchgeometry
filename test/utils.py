import torch
import numpy as np


# test utilites


def create_pinhole(fx, fy, cx, cy, height, width, rx, ry, rz, tx, ty, tz):
    """Creates pinhole model encoded to a torch.Tensor.
    """
    return torch.Tensor([
        [fx, fy, cx, cy, height, width, rx, ry, rz, tx, ty, tz]])


def create_checkerboard(h, w, nw):
    """Creates a synthetic checkerd board of shape HxW and window size `nw`.
    """
    return np.kron([[1, 0] * nw, [0, 1] * nw] * nw,
                   np.ones((h // (2 * nw), w // (2 * nw)))).astype(np.float32)


def create_eye_batch(batch_size, eye_size):
    """Creates a batch of identity matrices of shape Bx3x3
    """
    return torch.eye(eye_size).view(
        1, eye_size, eye_size).expand(batch_size, -1, -1)


def create_random_homography(batch_size, eye_size, std_val=1e-3):
    """Creates a batch of random homographies of shape Bx3x3
    """
    std = torch.FloatTensor(batch_size, eye_size, eye_size)
    eye = create_eye_batch(batch_size, eye_size)
    return eye + std.uniform_(-std_val, std_val)


def tensor_to_gradcheck_var(tensor, dtype=torch.float64, requires_grad=True):
    """Converts the input tensor to a valid variable to check the gradient.
      `gradcheck` needs 64-bit floating point and requires gradient.
    """
    assert torch.is_tensor(tensor), type(tensor)
    return tensor.requires_grad_(requires_grad).type(dtype)


def compute_mse(x, y):
    """Computes the mean square error between the inputs.
    """
    return torch.sqrt(((x - y) ** 2).sum())


def compute_patch_error(x, y, h, w):
    """Compute the absolute error between patches.
    """
    return torch.abs(x - y)[..., h // 4:-h // 4, w // 4:-w // 4].mean()


def check_equal_torch(a, b, eps=1e-4):
    return (torch.norm(a - b) <= (a.numel() * eps)).item()


def check_equal_numpy(a, b):
    return np.linalg.norm(a - b) <= (a.size * np.finfo(np.float32).eps)
