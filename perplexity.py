# Define presentation content
presentation_content = '''
# PyTorch: Powering the Future of AI

## Agenda
- Organization Background
- Research Activities
- Products and Features
- Evolution of PyTorch
- Future Roadmap

## Organization Background
- Developed by Meta AI (formerly Facebook's AI Research lab)
- Released in September 2016
- Python-based successor to Torch (Lua)
- Governed by PyTorch Foundation since September 2022

## Research Activities
- Computer Vision
- Natural Language Processing
- Deep Neural Networks
- Reinforcement Learning

## Products and Features
- Tensor computing (GPU-accelerated)
- Deep neural networks
- torch.nn module
- TorchScript
- TorchServe
- Distributed training

## Evolution of PyTorch
- 2016: Initial Release
- 2018: PyTorch 1.0
- 2023: PyTorch 2.0
- 2023: PyTorch 2.1
- 2024: PyTorch 2.2

## PyTorch 2.0 Highlights
- Faster model training speeds
- Support for Dynamic Shapes and Distributed training
- Optimizations for Graph Neural Networks (GNN)
- High-performance Transformer API implementation

## PyTorch 2.1 & 2.2 Features
### PyTorch 2.1:
- Automatic dynamic shape support in torch.compile
- torch.distributed.checkpoint for parallel saving/loading
- torch.compile support for NumPy API
- CPU performance improvements

### PyTorch 2.2:
- FlashAttention-v2 integration
- AOTInductor for ahead-of-time compilation
- Improved torch.compile support for Optimizers
- New logging mechanism (TORCH_LOGS)

## Future Roadmap
- Enhanced hardware support
- Integration of cutting-edge research
- User experience improvements
- Python 3.12 support
- FSDP2 (Fully Sharded Data Parallel) prototype
- Distributed pipelining
- Performance optimizations

## PyTorch's Impact on AI Development

## Questions?
''' 

# Convert to reveal.js format
slides = []

for section in presentation_content.split('## '):
    title = section.split('\n')[0].strip()
    content = '\n'.join(line.strip() for line in section.split('\n')[1:] if line.strip())
    slides.append(f'<section>\n<h2>{title}</h2>\n<p>{content}</p>\n</section>')

# Wrap in reveal.js HTML structure
reveal_js_content = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>PyTorch Presentation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://revealjs.com/css/reveal.css">
    <link rel="stylesheet" href="https://revealjs.com/css/theme/white.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {}    
        </div>
    </div>
    <script src="https://revealjs.com/js/reveal.js"></script>
    <script>
        Reveal.initialize();
    </script>
</body>
</html>
'''.format('\n'.join(slides))

reveal_js_content[:1000] # Display the first 1000 characters of the HTML