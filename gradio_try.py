import gradio as gr

# Define a function to display the uploaded image
def display_image(image):
    return image

# Create the Gradio interface
with gr.Blocks() as demo:
    image_input = gr.Image(type="pil", label="Upload an Image")
    image_output = gr.Image(label="Uploaded Image")

    # Set up the interaction
    image_input.change(fn=display_image, inputs=image_input, outputs=image_output)

# Launch the app
demo.launch(share = True)
