import discord, requests, random
from discord.ext import commands
import cv2


class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="FaceDetection", description="attempts to find a face in an image", aliases=["facedetect", "detectfaces"])
    async def FaceDetection(self, ctx):
        attachment_name = ctx.message.attachments[0].filename
        attachment_url = ctx.message.attachments[0].url
        r = requests.get(attachment_url)
        with open(f"./AI/{ctx.author.id}_{attachment_name}", "wb") as f:
            f.write(r.content)
        f.close()
        path_to_image = f"./AI/{ctx.author.id}_{attachment_name}"
        trained_face_data = cv2.CascadeClassifier('./AI/haarcascade_frontface.xml')
        img = cv2.imread(path_to_image)
        grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_coords = trained_face_data.detectMultiScale(grayscaled)
        for (x, y, w, h) in face_coords:
            cv2.rectangle(img, (x, y), (x+h, y+h), (random.randrange(256), random.randrange(256), random.randrange(256)), 2)
        cv2.imwrite(f"./AI/{ctx.author.id}_{attachment_name}", img)
        await ctx.send(file=discord.File(path_to_image))


def setup(client):
    client.add_cog(AI(client))
