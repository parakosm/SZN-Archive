from jinja2 import Environment, FileSystemLoader

# Define the directory where your templates are stored
# Assuming 'templates' folder is in the same directory as the script
template_dir = "jinjaninjas" 

# Create the Jinja environment
env = Environment(loader=FileSystemLoader(template_dir))

# Load the specific template file
template = env.get_template('index.html.jinja')

# Render the template
output_text = template.render()

#Save the rendered output
with open("//rcfs03.rosminicollege.school.nz/StudentsHome$/20062/Desktop/2026/Absolutely Not the Final Projeck/SZN Archive/renders/index.html", "w") as file:
    file.write(output_text)