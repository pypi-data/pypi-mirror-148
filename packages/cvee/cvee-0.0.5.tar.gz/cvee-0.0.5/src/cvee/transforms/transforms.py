import numpy as np
import torch


# TODO: maybe change it to a differentiable version
def transform(pts, tf_mat):
    """Apply a transformation matrix on a set of 3D points. Note that this function is not differentiable.

    Args:
        pts (np.ndarray, torch.Tensor): 3D points, could be Nx3 or BxNx3 (tensor only).
        tf_mat (np.ndarray, torch.Tensor): Transformation matrix, could be 4x4 or Bx4x4 (tensor only).

        The types of tf_mat and pts should be consistent.
    Returns:
        Transformed pts. Return torch.Tensor if matrix and points are torch.Tensor, else np.ndarray.
    """
    return_tensor = isinstance(tf_mat, torch.Tensor) or isinstance(pts, torch.Tensor)

    if not return_tensor:  # return np.ndarray
        new_pts = np.concatenate([pts, np.ones([pts.shape[0], 1])], axis=1)
        # `new_pts @ tf_mat.T` or `(tf_mat @ new_pts.T).T`
        new_pts = np.dot(new_pts, tf_mat.T)
        new_pts = new_pts[:, :3]
    else:  # return torch.tensor
        if tf_mat.ndim == 2 and pts.ndim == 2:
            new_pts = torch.cat([pts, torch.ones(pts.shape[0], 1).to(pts.device)], dim=1)
            new_pts = torch.mm(new_pts, torch.transpose(tf_mat, 0, 1))
            new_pts = new_pts[:, :3]
        elif tf_mat.ndim == 3 and pts.ndim == 3:
            padding = torch.ones(pts.shape[0], pts.shape[1], 1).to(pts.device)
            new_pts = torch.cat([pts, padding], dim=2)
            new_pts = torch.bmm(new_pts, torch.transpose(tf_mat, 1, 2))
            new_pts = new_pts[:, :, :3]
        else:
            raise RuntimeError(f"Incorrect size of tf_mat or pts, tf_mat: {tf_mat.shape}, pts: {pts.shape}")

    return new_pts


# TODO: write test cases
# TODO: add 4 x 4 input
def project(pts, intr_mat):
    """Project 3D points in the camera space to the image plane. Note that this function is not differentiable.

    Args:
        pts (np.ndarray, torch.Tensor): 3D points, could be Nx3 or BxNx3 (tensor only).
        intr_mat (np.ndarray, torch.Tensor): Intrinsic matrix, could be 3x3 or Bx3x3 (tensor only).

        The types of pts and intr_mat should be consistent.
    Returns:
        pixels, the order is uv other than xy.
        depth, depth in the camera space.
    """
    return_tensor = isinstance(intr_mat, torch.Tensor) or isinstance(pts, torch.Tensor)

    if not return_tensor:  # return np.ndarray
        pts = pts / pts[:, 2:3]
        new_pts = np.dot(intr_mat, pts.T).T
        return new_pts[:, :2]
    else:  # return torch.tensor
        if intr_mat.ndim == 2 and pts.ndim == 2:
            pts = pts.clone()
            pts = pts / pts[:, 2:3]
            new_pts = torch.mm(pts, torch.transpose(intr_mat, 0, 1))
            return new_pts[:, :2]
        elif intr_mat.ndim == 3 and pts.ndim == 3:
            pts = pts.clone()
            pts = pts / pts[..., 2:3]
            new_pts = torch.bmm(pts, torch.transpose(intr_mat, 1, 2))
            return new_pts[..., :2]
        else:
            raise RuntimeError(f"Incorrect size of intr_mat or pts: {intr_mat.shape}, {pts.shape}")


# TODO: implement this
def unproject():
    raise NotImplementedError()


# TODO: write test cases
def rot_tl_to_tf_mat(rot_mat, tl):
    """Build transformation matrix with rotation matrix and translation vector.

    Args:
        rot_mat (np.ndarray, torch.Tensor): rotation matrix, could be 3x3 or Bx3x3 (tensor only).
        tl (np.ndarray, torch.Tensor): translation vector, could be 3 or Bx3 (tensor only).
        The types of rot_mat and tl should be consistent.
    Returns:
        tf_mat, transformation matrix. Return torch.Tensor if rot_mat and tl are torch.Tensor, else np.ndarray.
    """
    return_tensor = isinstance(rot_mat, torch.Tensor) or isinstance(tl, torch.Tensor)

    if not return_tensor:  # return np.ndarray
        tf_mat = np.eye(4)
        tf_mat[:3, :3] = rot_mat
        tf_mat[:3, 3] = tl
        return tf_mat
    else:  # return torch.tensor
        if rot_mat.ndim == 2 and tl.ndim == 1:
            tf_mat = torch.eye(4)
            tf_mat[:, :3, :3] = rot_mat
            tf_mat[:, :3, 3] = tl
            return tf_mat
        elif rot_mat.ndim == 3 and tl.ndim == 2:
            batch_size = rot_mat.shape[0]
            tf_mat = torch.eye(4).unsqueeze(0)
            tf_mat = tf_mat.repeat(batch_size, 1, 1)
            tf_mat[:, :3, :3] = rot_mat
            tf_mat[:, :3, 3] = tl
            return tf_mat
        else:
            raise RuntimeError(f"Incorrect size of rot_mat or tl: {rot_mat.shape}, {tl.shape}")


# TODO: write test cases
def cart_to_homo(pts_3d):
    """Convert Cartesian 3D points to Homogeneous 4D points.

    Args:
      pts_3d (np.ndarray, torch.Tensor): 3D points in Cartesian coord, could be Nx3 or BxNx3 (tensor only).
    Returns:
      nx4 points in Homogeneous coord.
    """
    if isinstance(pts_3d, torch.Tensor):  # return np.ndarray
        return np.concatenate([pts_3d, np.ones([pts_3d.shape[0], 1])], axis=1)
    else:
        if pts_3d.ndim == 2:
            return torch.cat([pts_3d, torch.ones(pts_3d.shape[0], 1).to(pts_3d.device)], dim=1)
        else:
            padding = torch.ones(pts_3d.shape[0], pts_3d.shape[1], 1).to(pts_3d.device)
            return torch.cat([pts_3d, padding], dim=2)
