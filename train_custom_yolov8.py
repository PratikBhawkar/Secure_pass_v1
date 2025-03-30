# train_custom_yolov8.py

if __name__ == '__main__':
    from ultralytics import YOLO

    # Initialize the YOLO model with a base pretrained weight
    model = YOLO("yolov8n.pt")

    # Resume training from the latest checkpoint if available.
    # You can also lower the batch size if out-of-memory errors persist.
    results = model.train(
        data="indian_numberplates.yaml",  # Ensure this YAML file reflects your dataset paths
        epochs=100,                       # Total epochs you want to train for
        imgsz=640,                        # Image size for training
        batch=32,                         # You might need to lower this if memory issues continue
        project=".",                      # Save results in the current directory
        name="yolo_v8_custom_updated",    # Folder name for training artifacts
        resume=True                     # Resume training from last checkpoint
    )

    print("Training complete. Model and logs are saved in './yolo_v8_custom_updated'")
