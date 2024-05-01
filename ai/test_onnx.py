if __name__ == "__main__":
    import onnx
    import onnxruntime as ort
    
    print(ort.get_device())

    onnx_model = onnx.load("runs/detect/train15/weights/best.onnx")
    onnx.checker.check_model(onnx_model)
