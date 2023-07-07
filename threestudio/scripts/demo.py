# 1. Generate using StableDiffusionXL https://clipdrop.co/stable-diffusion

# 2. Remove background https://clipdrop.co/remove-background

# 3. Resize to 512x512 https://www.iloveimg.com/resize-image

# 4. Estimate depth and normal https://omnidata.vision/demo/ (I used Omnidata Normal (with X-TC & 3DCC), and MiDaS Depth)


# 5. Convert depth image from RGB to greyscale
def depth_rgb_to_grey(depth_filename):
    # depth_filename = "image_depth.png"
    import cv2
    import numpy as np

    # import shutil
    # shutil.copyfile(depth_filename,  depth_filename.replace("_depth", "_depth_orig"))
    depth = cv2.imread(depth_filename)
    depth = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
    mask = (
        cv2.resize(
            cv2.imread(depth_filename.replace("_depth", "_rgba"), cv2.IMREAD_UNCHANGED)[
                :, :, -1
            ],
            depth.shape,
        )
        > 0
    )
    # depth[mask] = (depth[mask] - depth.min()) / (depth.max() - depth.min() + 1e-9)
    depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-9)
    depth[~mask] = 0
    depth = (depth * 255).astype(np.uint8)
    cv2.imwrite(depth_filename, depth)


# 6. Mask normal
def normal_mask(normal_filename):
    # filename = "image_normal.png"
    import cv2

    # import shutil
    # shutil.copyfile(normal_filename, normal_filename.replace("_normal", "_normal_orig"))
    normal = cv2.imread(normal_filename)
    mask = (
        cv2.resize(
            cv2.imread(
                normal_filename.replace("_normal", "_rgba"), cv2.IMREAD_UNCHANGED
            )[:, :, -1],
            normal.shape[:2],
        )
        > 0
    )
    normal[~mask] = 0
    cv2.imwrite(normal_filename, normal)


# 5. Run Zero123
# python launch.py --config configs/zero123.yaml --train --gpu 0 system.loggers.wandb.enable=true system.loggers.wandb.project="voletiv-zero123XL-demo" system.loggers.wandb.name="grootplant_64_128_d0.05_drel_OLD" data.image_path=./load/images/grootplant_rgba.png system.freq.guidance_eval=0 system.guidance.pretrained_model_name_or_path="./load/zero123/105000.ckpt" tag='${data.random_camera.height}_${rmspace:${basename:${data.image_path}},_}_OLD'
# python launch.py --config configs/zero123.yaml --train --gpu 1 system.loggers.wandb.enable=true system.loggers.wandb.project="voletiv-zero123XL-demo" system.loggers.wandb.name="grootplant_64_128_d0.05_drel" data.image_path=./load/images/grootplant_rgba.png system.freq.guidance_eval=0 system.guidance.pretrained_model_name_or_path="./load/zero123/XL_20230604.ckpt" tag='${data.random_camera.height}_${rmspace:${basename:${data.image_path}},_}_XL'
