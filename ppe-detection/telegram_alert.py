from telegram import Bot
import matplotlib.pyplot as plt
from io import BytesIO
import subprocess

BOT_TOKEN = "xxx"
CHAT_ID = ["xxx", "xxx"]
helmet = "helmet"

message = (
            "⚠️ Safety Gear Alert!\n"
            f"VisionAI has detected a worker without a {helmet}. Please address this safety violation immediately."
)

def create_bar_chart():
    labels = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 
              'NO-Safety Vest', 'Person', 'Safety Cone', 
              'Safety Vest', 'Machinery', 'Vehicle']
    values = [2, 1, 2, 0, 0, 0, 0, 0, 0, 0]

    # Sorting the data in descending order
    sorted_data = sorted(zip(labels, values), key=lambda x: x[1], reverse=True)
    labels, values = zip(*sorted_data)

    fig, ax = plt.subplots()

    # Creating a bar plot with different colors for each bar
    ax.bar(labels, values, color=['blue', 'red', 'green'])

    # Adding labels and title
    ax.set_ylabel('Counts')
    ax.set_title('Safety Gear Detection')

    # Adding a grid on y-axis
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.7)

    # Setting 4 ticks on the y-axis
    plt.yticks([0, 1, 2, 3])

    # Making x-axis labels readable
    plt.xticks(rotation=45, fontsize=8, ha='right')

    # Adding value labels on top of the bars
    for i, v in enumerate(values):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

    # Save the plot to a file
    plt.savefig('chart.png', bbox_inches='tight')
    plt.close(fig)

def get_ip_address():
    try:
        ip_address = subprocess.check_output(
            "ifconfig | grep \"inet \" | grep -Fv 127.0.0.1 | awk '{print $2}'", shell=True
        ).decode("utf-8").strip()
        return ip_address
    except subprocess.CalledProcessError:
        return "Could not get IP address"
    
def send_telegram_alert(message, chat_ids):
    bot = Bot(token=BOT_TOKEN)
    create_bar_chart()  # This will create 'chart.png' in your script's directory
    
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=message)
        bot.send_photo(chat_id=chat_id, photo=open('chart.png', 'rb'))

def send_telegram_ip(message, chat_ids):
    bot = Bot(token=BOT_TOKEN)
    ip_message = f"IP Address: http://{get_ip_address()}:5000/"

    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=ip_message)

# define_IP = ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}'

if __name__ == "__main__":
    send_telegram_ip(message, CHAT_ID)
    send_telegram_alert(message, CHAT_ID)

