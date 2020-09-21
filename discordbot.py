from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


class RoleDeal:

    def __init__(self):
        self.channel_mem = []
        self.mem_len = 0
        self.vc_state_err = '実行できません。ボイスチャンネルに入ってコマンドを実行してください。'

    def set_mem(self, ctx):
        state = ctx.author.voice # コマンド実行者のVCステータスを取得
        if state is None:
            return False

        self.channel_mem = [i.name for i in state.channel.members] # VCメンバリスト取得
        self.mem_len = len(self.channel_mem) # 人数取得
        while self.mem_len % 5 != 0:
            self.channel_mem.append('ノラ')
        return True

    # チーム数を指定した場合のチーム分け
    def team_role_deal(self, ctx, remainder_flag='false'):
        team = []
        
        if self.set_mem(ctx) is False:
            return self.vc_state_err
        
        # チーム数を取得
        party_num = self.mem_len // 5

        # メンバーリストをシャッフル
        random.shuffle(self.channel_mem)

        # チーム分け
        for i in range(party_num): 
            team.append("<<<<< チーム"+str(i+1)+" >>>>>")
            team.extend(self.channel_mem[i:self.mem_len:party_num])

        return ('\n'.join(team))


@bot.event
async def on_ready():
    print('-----Logged in info-----')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------------------------')

# メンバー数を指定してチーム分け
@bot.command()
async def deal(ctx):
    role_deal = RoleDeal()
    msg = role_deal.make_specified_len(ctx)
    await ctx.channel.send(msg)


bot.run(token)
