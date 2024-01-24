import xcord

activit=[
    xcord.activity("$math[1+1]"),
    xcord.activity("$math[2+2]",activity=2)
]
bot=xcord.xcordisnake(activity=activit,activity_second=10)
bot.activity_start()

bot.onReady(
    code="$print[$botname[]]"
)

bot.command(
    name="test",
    description="hi",
    code="""
$defer[]
$let[item;[1,2,3]]
$for[$get[item];$print($get[i])]
$excordt_response[Hello World!]
"""
)

bot.command(
    name="test2",
    description="welcome",
    code="""
$let[item;[1,2,3]]
$for[$get[item];$print($get[i])]
$send_response[Hello World!]
"""
)

# https://vectips.com/wp-content/uploads/2017/03/project-preview-large-2.png


bot.command(
    name="test_emb",
    description="embed",
    commands=[{"name":"arg","description":"Test!","required":True}],
    code="""
$defer[]
$title[1;$authorID[]]
$description[1;test2]
$footer[1;test3]
$image[1;https://vectips.com/wp-content/uploads/2017/03/project-preview-large-2.png]
$author[1;sadsd]
$thumbnail[1;https://vectips.com/wp-content/uploads/2017/03/project-preview-large-2.png]
$addfield[1;test;TEST TEXT]
$color[1;RED]
$embed[1]
$excordt_response[Hello World!;1]
"""
)

bot.run("-----InSeRt YoUr ToKeN-----")
