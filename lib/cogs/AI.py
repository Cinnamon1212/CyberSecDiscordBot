import discord, requests, random, sys, json, math, datetime, os, magic, cv2
from discord.ext import commands
from discord import Embed
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model

wilfredOwenModel = load_model("./AI/wilfredowen.model")
poetryText = open("./AI/wilfredowen.txt", "r").read().lower()

async def facedetect_f(ctx, attachment_name, path_to_image):
    trained_face_data = cv2.CascadeClassifier('./AI/haarcascade_frontface.xml')
    img = cv2.imread(path_to_image)
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_coords = trained_face_data.detectMultiScale(grayscaled)
    for (x, y, w, h) in face_coords:
        cv2.rectangle(img, (x, y), (x+h, y+h), (random.randrange(256), random.randrange(256), random.randrange(256)), 2)
    cv2.imwrite(f"./AI/{ctx.author.id}_{attachment_name}", img)

async def probGenerator(preds, temp):
    # https://github.com/dgibbs2016/Shakespeare-in-LSTM/blob/c7e1399c92b794bbcacbd754b4e47c53682de313/lstm_text_generation.py#L62
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temp
    expPreds = np.exp(preds)
    preds = expPreds / np.sum(expPreds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

async def textGenerator(length, temperature, text, SEQ_LENGTH, characters, index_to_char, char_to_index):
    start_index = random.randint(0, len(text) - SEQ_LENGTH - 1)
    generated = ''
    sentence = text[start_index: start_index + SEQ_LENGTH]
    generated += sentence
    for i in range(length):
        x_predictions = np.zeros((1, SEQ_LENGTH, len(characters)))
        for t, char in enumerate(sentence):
            x_predictions[0, t, char_to_index[char]] = 1

        predictions = wilfredOwenModel.predict(x_predictions, verbose=0)[0]
        next_index = await probGenerator(predictions, temperature)
        next_character = index_to_char[next_index]

        generated += next_character
        sentence = sentence[1:] + next_character
    return generated

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="FaceDetection", description="attempts to find a face in an image", aliases=["facedetect", "detectfaces"])
    async def FaceDetection(self, ctx):
        text = "Usage: ./FaceDetect // Attach a file"
        if ctx.message.attachments:
            attachment_name = ctx.message.attachments[0].filename
            extension = attachment_name.split(".")[-1]
            accepted_extensions = ["png", "jpeg", "jpg", "bmp"]
            if "/" in attachment_name:
                await ctx.send(f"```Filenames cannot contain /\'s \n{text}```")
            elif extension not in accepted_extensions:
                await ctx.send(f"```Unaccepted file extension\n{text}```")
            else:
                attachment_url = ctx.message.attachments[0].url
                r = requests.get(attachment_url)
                with open(f"./AI/{ctx.author.id}_{attachment_name}", "wb") as f:
                    f.write(r.content)
                path_to_image = f"./AI/{ctx.author.id}_{attachment_name}"
                accepted_mimes = ["image/jpeg", "image/jpg", "image/png", "image/bmp"]
                if magic.from_file(path_to_image, mime=True) in accepted_mimes:
                    await facedetect_f(ctx, attachment_name, path_to_image)
                    await ctx.send(file=discord.File(path_to_image))
                else:
                    await ctx.send(f"```Unsupported file type!\n{text}```")
                    os.remove(path_to_image)
        else:
            await ctx.send(f"```Please attach an image\n{text}```")

    @commands.command(name="wilfredowen", description="Use AI to generate a poem in the style of wilfred owen")
    async def wilfredowen(self, ctx, charCount: int = 300):
        if charCount > 500:
            await ctx.send(f"```You can only use a maximum of 500 characters```")
        else:
            SeqLen = 40
            StepSize = 3
            charSet = sorted(set(poetryText))
            charToIndex = dict((c, i) for i, c in enumerate(charSet))
            indexToChar = dict((i, c) for i, c in enumerate(charSet))
            generatedText = await textGenerator(300, 1.0, poetryText, SeqLen, charSet, indexToChar, charToIndex)
            await ctx.send(f"```{generatedText}```")

    @wilfredowen.error
    async def wilfredowen_error(self, ctx, error):
        text = "Usage: ./wilfredowen (character count)"
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"```{text}```")
        else:
            await ctx.send(f"```An unknown error has occured\n{text}```")
            raise error


def setup(client):
    client.add_cog(AI(client))
