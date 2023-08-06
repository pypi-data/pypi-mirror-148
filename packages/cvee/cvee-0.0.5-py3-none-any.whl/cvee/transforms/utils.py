import numpy as np
import torch


# TODO: implement this
def fov_to_intrinsic(fov, width, height):
    pass


# TODO: implement this
def intrinsic_to_fov(matrix):
    pass


# TODO: implement this
def look_at_view_transform(dist=1.0, elev=0.0, azim=0.0, degrees=True, return_tensor=False):
    """This function returns a transformation matrix (camera pose)
    to apply the 'Look At' transformation from view -> world coordinates [0].

    Args:
        dist (float): Distance of the camera from the object.
        elev (float): The angle between the vector from the object to the camera,
            and the horizontal plane z = 0 (xy-plane).
        azim (float): The vector from the object to the camera is projected onto a horizontal plane z = 0 (xy-plane).
            azim is the angle between the projected vector and a reference vector at (1, 0, 0)
            on the reference plane (the horizontal plane).
        degrees (bool, optional): If the elevation and azimuth angles are specified in degrees or radians.
        return_tensor (bool, optional): Return torch.tensor or np.array.

    Returns:
        Transform matrix. Return torch.tensor if return_tensor is True, else np.ndarray.

    References:
    [0] https://www.scratchapixel.com
    """
    pass


# TODO: change to np.mgrid
def create_grid(origin=None, size=None, resolution=None, return_tensor=False):
    """Create a 3D grid.

    Args:
        origin (list, optional): The (bottom, left, back) corner of the grid,
            note that it's not the center
        size (list, optional): The 3D size of the grid.
        resolution (list, optional): The resolution of the grid.
        return_tensor (bool, optional): Return `torch.tensor` or `np.array`.

    Returns:
        The points in the 3D grid.
    """

    if origin is None:
        origin = [-0.5, -0.5, -0.5]
    if size is None:
        size = [1.0, 1.0, 1.0]
    if resolution is None:
        resolution = [64, 64, 64]

    x = np.linspace(origin[0], origin[0] + size[0], resolution[0])
    y = np.linspace(origin[1], origin[1] + size[1], resolution[1])
    z = np.linspace(origin[2], origin[2] + size[2], resolution[2])

    xv, yv, zv = np.meshgrid(x, y, z, indexing="ij")
    points = np.concatenate([xv[..., None], yv[..., None], zv[..., None]], axis=-1).astype(np.float32)

    if return_tensor:
        # we do not use `torch.meshgrid` since its api is not stable currently
        points = torch.from_numpy(points).float()

    return points
