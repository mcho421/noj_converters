#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from StringIO import StringIO
import unittest
from textwrap import dedent
from pyparsing import *
from daijirin2_grammar import *
from noj.misc.uni_printer import UniPrinter

class TestDaijirin2(unittest.TestCase):

    def test_entry_headers(self):
        test_entries = dedent(u"""\
            <INDENT=1><PAGE><HEAD>――言えばこう言う</HEAD>
            <INDENT=1><PAGE><HEAD>あ</HEAD> [1] （感）
            <INDENT=1><PAGE><HEAD>アーカイブ</HEAD> [3] 〖archive〗
            <INDENT=1><PAGE><HEAD>アーケイック</HEAD> [4][3] 〖archaic〗 （形動）
            <INDENT=1><PAGE><HEAD>ああ-しやごしや</HEAD> （連語）
            <INDENT=1><PAGE><HEAD>あい-こ</HEAD> アヒ― [0][3]
            <INDENT=1><PAGE><HEAD>ひ-い・でる</HEAD> [3] 【秀でる】 （動ダ下一）[文]ダ下二 ひい・づ
            <INDENT=1><PAGE><HEAD>する</HEAD> [0] 【為る】 （動サ変）[文]サ変 す
            <INDENT=1><PAGE><HEAD>スルホン-か</HEAD> ―クワ [0] 【―化】
            <INDENT=1><PAGE><HEAD>ずる-やすみ</HEAD> [3] 【ずる休み】 （名）スル
            <INDENT=1><PAGE><HEAD>ず-ろう</HEAD> ヅ― [0] 【杜漏】 （名・形動）[文]ナリ
            <INDENT=1><PAGE><HEAD>す-ろうにん</HEAD> ―ラウニン [2] 【素浪人】
            <INDENT=1><PAGE><HEAD>せい-えん</HEAD> [0] 【清艶・清婉】 （名・形動）[文]ナリ
            <INDENT=1><PAGE><HEAD>けしうはあら∘ず</HEAD>
            <INDENT=1><PAGE><HEAD>こう-えい</HEAD> クワウ― [0] 【光栄】 （名・形動）スル [文]ナリ
            <INDENT=1><PAGE><HEAD>ちょう-じょう</HEAD> ―デフ [0] 【重畳】 (ト|タル)スル[文]形動タリ
            <INDENT=1><PAGE><HEAD>いす</HEAD> （助動）(いせ（いしよ・いし）・いし・いす・いす・いすれ・いし)
            <INDENT=1><PAGE><HEAD>ごとく-なり</HEAD> 【如くなり】 （助動）(ごとくなら・ごとくなり（ごとくに）・ごとくなり・ごとくなる・ごとくなれ・ごとくなれ)
            <INDENT=1><PAGE><HEAD>あい-しらい</HEAD> アヒシラヒ
            <INDENT=1><PAGE><HEAD>いおう-に-むにん</HEAD> ―ワウ― [1]-[0][0]-[0] 【易往而無人】
            <INDENT=1><PAGE><HEAD>あらわ・れる</HEAD> アラハレル [4] 【表れる（表われる）・現れる（現われる）・顕れる】 （動ラ下一）[文]ラ下二 あらは・る
            <INDENT=1><PAGE><HEAD>おぼこ</HEAD> [0] （名・形動）[文]ナリ
            <INDENT=1><PAGE><HEAD>きゅうり-がく</HEAD> キユウ―・キウ― [3] 【窮理学・究理学】
            <INDENT=1><PAGE><HEAD>カラクン-ちょう</HEAD> ―テウ 【―鳥・唐国鳥】
            <INDENT=1><PAGE><HEAD>シナ-よもぎ</HEAD> [3] 【―蓬・―艾】
            <INDENT=1><PAGE><HEAD>あら-おこし</HEAD> [3] 【荒起(こ)し・粗起(こ)し】 （名）スル
            <INDENT=1><PAGE><HEAD>びりょう-ようそ</HEAD> [4] ―リヤウヤウ― 【微量養素】 ・ ―リヤウエウ― 【微量要素】
            <INDENT=1><PAGE><HEAD>とう-とう</HEAD> [0] トウトウ 【鼕鼕】 ・ タウタウ 【鏜鏜】 ・ タウタフ 【鞺鞳】 (ト|タル)[文]形動タリ
            """).splitlines()

        for e in test_entries:
            print e
            res = (ENTRY_HEADER + stringEnd).parseString(e)
            dump = res.dump()
            pp.pprint(dump)
            print

    def test_all_entry_headers(self):
        i = 0
        with codecs.open('daijirin2_entry_headers', 'r', 'utf-8') as f:
            for line in f:
                i += 1
                line = line.rstrip()
                # if i > 80000:
                # print i, line
                d = (ENTRY_HEADER + stringEnd).parseString(line).dump()
                # pp.pprint(d)
                # print
                if i % 1000 == 0:
                    print i

    def test_entries(self):
        test_entries = [
            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あ</HEAD>
            <INDENT=4>（１）五十音図ア行第一段の仮名。後舌の広母音。
            （２）平仮名「あ」は「安」の草体。片仮名「ア」は「阿」の行書体の偏。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あ</HEAD> 【足】
            <INDENT=4>あし。「―の音せず行かむ駒もが/万葉 3387」
            〔多く「足掻(アガ)き」「足結(アユイ)」など，複合した形で見られる〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あ</HEAD> 【畔・畦】
            <INDENT=4>田のあぜ。「営田(ツクダ)の―を離ち/古事記（上）」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あ</HEAD> 【阿】
            <INDENT=4>〔梵 a〕
            梵語の第一字母の音訳。
            <LINK>⇔吽(ウン)</LINK[139570:832]>
            <LINK>→阿字</LINK[138042:1938]>
            <LINK>→梵字</LINK[154550:1152]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>ああ</HEAD> [0] （副）
            <INDENT=4>（１）ある場面の様子をさしていう。話し手からやや離れた場面や，話している時点とは別の場面などについていう。「―はなりたくない」「―うるさくては，かなわない」「ちょっと目を離すとすぐ―だ」
            （２）話した内容や心の中で考えたことがらなどをさす。「―でもないこうでもない」「―言っておいたから，大丈夫だろう」
            〔「ああだ」「ああでも」「ああは」などの場合，アクセントは [1]〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーク-ねつ</HEAD> [3] 【―熱】
            <INDENT=4>アーク放電の際に出る高熱。摂氏三〇〇〇度以上に達する。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーケイック</HEAD> [4][3] 〖archaic〗 （形動）
            <INDENT=4><LINK>⇒アルカイック</LINK[138391:1160]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーチェリー</HEAD> [1] 〖archery〗
            <INDENT=4>（１）ヨーロッパで発達した弓術。また，それに用いる弓。洋弓。
            （２）洋弓を用いるスポーツ。標的（ターゲット）をねらい射って，得点を争う。
            <FIG>アーチェリー（１）</FIG>[図]
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あいおい-むすび</HEAD> アヒオヒ― [5] 【相生結び】
            <INDENT=4>ひもの飾り結びの一。女結びの一端をさらにその結び目に通したもの。
            <FIG>相生結び</FIG>[図]
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーティフィシャル</HEAD> [3] 〖artificial〗 （形動）
            <INDENT=4>人工的であるさま。人為的。不自然。
            <LINK>⇔ナチュラル</LINK[151164:190]>
            「―-ライト（＝人工光線）」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーノルド</HEAD> 〖Arnold〗
            <INDENT=4>（１）〔Edwin A.〕
            (1832-1904) イギリスの詩人。釈迦の生涯・教義を長編無韻詩「アジアの光」に著した。
            （２）〔Matthew A.〕
            (1822-1888) イギリスの詩人・批評家。文明批評にまで発展させた「教養と無秩序」のほか，「批評論集」などの著がある。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アーリア-じん</HEAD> [4] 【―人】
            <INDENT=4>〔貴い，の意の梵語 ārya から。アーリヤ人とも〕
            （１）インド-ヨーロッパ語族に属する言語を話し，紀元前1500年頃中央アジアからインドやイランに移住した古代民族。現代のヨーロッパやアジアの多くの民族と文化的共通性をもつ。
            （２）ナチスが用いた人種分類の一。起源を異にするセム（ユダヤ）人に対し，アーリア人であるゲルマン民族の優越が主張された。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい</HEAD> アヒ 【合(い)】
            <INDENT=4>名詞の下に付いて，接尾語的に用いる。
            （１）「ようす」「ぐあい」などの意を表す。「色―」「肌―」
            （２）意味をぼかして，婉曲(エンキヨク)な表現にする。「意味―」「義理―」
            （３）互いにその動作をする意を表す。「にらみ―」「果し―」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい</HEAD> [1] 【愛】
            <INDENT=4>（１）対象をかけがえのないものと認め，それに引き付けられる心の動き。また，その気持ちの表れ。（ア）相手をいつくしむ心。相手のために良かれと願う心。「子への―」「―を注ぐ」「―の手をさしのべる」（イ）異性に対して抱く思慕の情。恋。「―が芽生える」「―を告げる」「―をはぐくむ」（ウ）何事にもまして，大切にしたいと思う気持ち。「学問に対する―」
            （２）キリスト教で，神が人類を限りなく深くいつくしむこと。
            <LINK>→アガペー</LINK[137917:1496]>
            （３）〔仏〕 人や物にとらわれ，執着すること。むさぼり求めること。渇愛。
            （４）他人に好ましい印象を与える容貌や振る舞い。あいそ。あいきょう。「阿呆口たたけば，夫が―に為つて/滑稽本・浮世風呂 4」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい</HEAD> アヒ 【相】
            <INDENT=4>〔「あい（合）」と同源〕
            ■一■ （接頭）
            （１）名詞に付いて，「同じ」という意を表す。「―弟子」「―部屋」
            （２）動詞に付いて，互いに，ともに，の意を表す。「―対する」「―語らう」
            （３）動詞に付いて，語調を整え，また意味を強める。「婚儀が―調いました」「この結末はいかが―成るか」
            ■二■ （名）
            （１）二人が互いに槌(ツチ)で物を打つこと。あいづち。［和名抄］
            （２）仲間。同類。ぐる。「むむ，扨は―ぢやの/浄瑠璃・吉野都女楠」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アイーダ</HEAD> 〖Aida〗
            <INDENT=4>ベルディ作曲のオペラ。四幕。エジプトにとらわれたエチオピア王女アイーダとエジプトの将軍ラダメスとの悲恋物語。スエズ運河の開通を記念して1871年カイロで初演。
            <WAV>→「アイーダ」より行進曲（ベルディ）[音声]</WAV>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アイ-エム-エフ</HEAD> 〖 IMF 〗
            <INDENT=4>（１）〔International Monetary Fund〕
            国際通貨基金。第二次大戦後の国際通貨制度の安定を目指すブレトンウッズ協定に基づき，1945年12月に発足した国連の専門機関。加盟国は出資義務を負い，金・ドルを基軸とする固定相場制の下，為替取引を自由化し，国際収支が悪化した国は資金の融通を受けられるとされたが，1973年以降の変動相場制への移行に伴い，発展途上国への融資機関としての性格を強めている。日本は52年に加盟。
            （２）〔International Metalworkers Federation〕
            <LINK>⇒国際金属労連(コクサイキンゾクロウレン)</LINK[144073:1778]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-ぎょう</HEAD> ―ゲウ [0] 【愛楽】 （名）スル
            <INDENT=4>（１）〔仏〕（仏法などを）願い求めること。
            （２）愛し好むこと。「人に―せられずして衆にまじはるは恥なり/徒然 134」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-くるし・い</HEAD> [5] 【愛くるしい】 （形）[文]シク あいくる・し
            <INDENT=4>（子供や若い女性が）たいへんかわいらしい。「―・い笑顔」
            [派生] ――げ（形動）――さ（名）
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-ご</HEAD> [1] 【愛語】
            <INDENT=4>〔仏〕
            〔梵 priya-vāditā-saṃgraha〕
            四摂法(シシヨウボウ)の一。仏道に導くため，親しみの気持ちを抱くような心のこもった言葉をかけること。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-ご</HEAD> [1] 【愛護】 （名）スル
            <INDENT=4>（１）かわいがって，大事にすること。「動物―週間」「余が女を―せざるはなし/花柳春話（純一郎）」
            （２）〔「愛護の若」の主人公の髪形から〕
            歌舞伎の稚児役のつける鬘(カツラ)。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-さつ</HEAD> [1] 【挨拶】 （名）スル
            <INDENT=4>□一□
            （１）人と人とが出会ったときや，別れるときに交わす儀礼的な動作や言葉。また，その言葉を述べること。相手に敬意・親愛の意を示す行為で，対人関係を円満にし，社会生活を円滑にする。「初対面の人と―する」「時候の―」「―を返す」
            （２）公の席や舞台などで，大勢の人に向かって祝いやお礼などの気持ちを述べる言葉。「披露宴で―する」「就任の―」
            （３）受け答え。応対。返答。「手紙をやったのに何の―もない」「あのようにけんもほろろでは―のしようもない」
            （４）儀礼的な通知。「―状」
            （５）（「御挨拶」の形で）あきれた言いざま。
            <LINK>→ごあいさつ</LINK[143648:1608]>
            （６）「仕返し」をいう不良仲間の隠語。「あとで―に行くからな」
            □二□
            （１）禅宗で，門下の僧と問答をして悟りの程度を知ること。
            （２）二人の仲。交際。関係。「二郎兵衛殿とおきさ殿―見ればうら山しうて堪らぬ/浄瑠璃・今宮心中（中）」
            （３）仲介。仲裁。調停。また，その人。「さう見受ましたから―に這入りました/歌舞伎・お染久松色読販」
            〔「挨」も「拶」も押すことで，押し合う意から。もと禅宗用語で，□二□（１）が原義〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい・す</HEAD> [1] 【愛す】
            <INDENT=4>■一■ （動サ五）
            〔サ変動詞「愛する」の五段化〕
            「愛する」に同じ。「いつまでも―・されたい」「自然を―・す心」
            [可能] あいせる
            ■二■ （動サ変）
            <LINK>⇒あいする</LINK[137812:966]>
            〔口頭語では五段活用が優勢で，未然形は「愛さない」「愛される」のように「愛さ」が普通。終止形・連体形は五段の「愛す」，サ変の「愛する」の両方が用いられる。「愛すべし」の場合は文語のサ変「愛す」の終止形が用いられたもの〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>うな-うな</HEAD>
            <INDENT=4>〔幼児語〕〔「うな」は「汝(ウヌ)は」の転〕
            「うな」と言ってしかること。おどししかること。「にくいおつかあめだの。―をしてやらう/滑稽本・浮世風呂（前）」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>ガムラン</HEAD> [1][0] 〖(マレー) gamelan〗
            <INDENT=4>インドネシアのジャワやバリの伝統音楽。ゴングやガンバン（木琴）などを中心とする器楽合奏。舞踊劇や影絵芝居の伴奏に用いられる。
            <WAV>→ガムラン[ジャワ][音声]</WAV>
            <WAV>→ガムラン[バリ][音声]</WAV>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あい-にく</HEAD> [0] 【生憎】
            <INDENT=4>〔「あやにく」の転〕
            ■一■ （形動）[文]ナリ
            期待や目的にそわない状況になって，都合が悪く残念なさま。自分の場合にも，相手の気持ちを思いやる場合にも用いる。「―なお天気です」「―の雨で一歩も外へ出られなかった」
            <LINK>→おあいにくさま</LINK[139900:1498]>
            ■二■ （副）
            都合の悪いことに。折あしく。「―（と）留守をしていて失礼しました」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>い・る</HEAD> [0] 【入る】
            <INDENT=4>■一■ （動ラ五［四］）
            ❶人などが意図的に内側に移動する。
            （１）人などが，ある建物・区画の中に移動する。はいる。「無用の者―・る可(ベ)からず」「虎穴に―・らずんば虎子を得ず」
            （２）京都の町で場所を示す場合に，南北の通りから西または東へ少し行く。「中京区丸太町通り寺町東―・る」
            （３）人が，ある分野に進む。…の一員となる。「仏門に―・る」
            （４）人が，ある精神的状態になる。「涅槃(ネハン)に―・る」「悟道に―・る」
            ❷物などが内側に移動する。また，物の内部に何かが生ずる。
            （１）物が何かの中にはいる。抽象的なものについてもいう。「ずいぶん念が―・っている」「病(ヤマイ)膏肓(コウコウ)に―・る」「すずりに髪の―・りてすられたる/枕草子 28」
            （２）太陽・月が没する。「月ガ―・ッタ/ヘボン（三版）」
            （３）（「ひびがいる」の形で）割れ目が生ずる。「茶碗にひびが―・る」「骨にひびが―・ったらしい」
            ❸事態が進行して，ある状態になる。「話はいよいよ佳境に―・った」「悦(エツ)に―・る」
            ❹ある時刻・季節になる。「寒(カン)に―・る」
            ❺他の動詞の下に付いて複合動詞をつくる。
            （１）自然にその状態になりきる意を表す。「消え―・りそうな声」「寝―・る」
            （２）意図的にその動作に徹する意を表す。「話に聞き―・る」「恐れ―・ります」
            〔「はいる」のやや古めかしい言い方。「いれる」に対する自動詞〕
            ■二■ （動ラ下二）
            <LINK>⇒いれる</LINK[139066:1486]>
            [慣用] 有卦(ウケ)に―・悦に―・寒に―・気に―・技(ギ)神(シン)に―・鬼籍に―・御意(ギヨイ)に―・興に―・神(シン)に―・手に―・堂に―
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>の・べる</HEAD> [2] 【伸べる・延べる】 （動バ下一）[文]バ下二 の・ぶ
            <INDENT=4>❶長さを長くする。のばす。
            （１）ある人に向かって手などをのばす。さしのべる。「手を―・べる」
            （２）物を押しつぶして平らにのばしたり，たたんであった物を広げたりする。「紙を―・べて詩を書く」「床を―・べる」
            （３）曲がっていたものをまっすぐにする。のばす。「私ざまには腰―・べて，など，ものの聞こえひがひがしかるべきを/源氏（須磨）」
            ❷時間・期限をのばす。
            （１）期日・期限をもっと先にする。くりのべる。延期する。「修法―・べさすべかりけり/源氏（賢木）」
            （２）命を長くする。「かつは齢をも―・べむと思ほして/源氏（絵合）」
            ❸心身をゆったりさせる。「げに古ごとぞ人の心を―・ぶるたよりなりける/源氏（総角）」
            ❹水などを加えて液の濃度を薄くして量をふやす。のばす。「汁の味噌の濃きは湯にて―・ぶる/仮名草子・尤之草紙」
            〔「伸びる」に対する他動詞〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アイガー</HEAD> 〖Eiger〗
            <INDENT=4>スイス中部，アルプス山脈の高峰。海抜3970メートル。北壁は登攀(トウハン)困難な岩壁として有名。
            <FIG>アイガー（グロスシャイデックより）</FIG>[カラー図版]
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あいだ</HEAD> アヒダ [0] 【間】
            <INDENT=4>（１）二つのものにはさまれた，あいている部分。中間。「駅から家までの―に停留所が二つある」「本の―にしおりをはさむ」「雲の―から月が見える」「体重は常に五〇キロから五五キロの―だ」
            （２）ある範囲によって限られた一続きの時間。「七時から八時までの―に食事をとる」「夏休みの―にまとまった仕事を片付ける」「勉強している―に夜が明けた」「長い―かかって作品を仕上げる」
            （３）ものとものとを隔てる空間，または時間。間隔。へだたり。ま。「二，三〇センチの―を置いて苗を植える」「行(ギヨウ)と行との―をあける」「―を置いて雷鳴が聞こえる」
            （４）相対する二つの対象の関係。「日本と西欧の―には，歴史や文化に大きな相違がある」「横綱と大関の―にはあまり力の差はない」
            （５）複数の事物が構成する一つのまとまり。「政治家の―では常識だ」「生徒の―に流行している遊び」
            （６）人と人，ものとものの関係。間柄。仲。「二人の―は親も認めている」
            （７）二つのものの平均。中間。「双方の主張の―をとって」
            （８）大体の範囲。およその見当。あたり。頃。「やうやう，朱雀の―に，この車につきて/平中 25」「五六歳に成る―，泥土を以て仏の像を造り/今昔 11」
            （９）二つの事物のうちどちらか。「宮中の大臣共を召されて鹿・馬の―を御尋ね候べし/太平記 26」
            （１０）（形式名詞）
            活用語の連体形に付いて，接続助詞のように用いる。記録体・和漢混交文に多く用いられた。（ア）単に前の叙述を後の叙述に続ける。ところ。「鹿を射むと思て待ち立てりし―，俄(ニワカ)に虎来て喰らはんとせし時/今昔 1」（イ）前の叙述が後の叙述の理由・原因であることを表す。ゆえに。「後に，さかしき人々書きいれたる―，物語多くなれり/宇治拾遺（序）」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あいつ</HEAD> [0] 【彼奴】 （代）
            <INDENT=4>〔「あやつ」の転〕
            遠慮のない相手との会話や，親しみ・憤り・侮蔑(ブベツ)などの気持ちを表すときに用いる。
            （１）三人称。彼または彼女。やつ。「―は実にいい奴だ」
            （２）遠称の指示代名詞。あれ。「―よりこいつの方が安くていい」
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あお・い</HEAD> アヲイ [2] 【青い・蒼い】 （形）[文]ク あを・し
            <INDENT=4>（１）青の色をしている。広く緑など青系統の色にもいう。「―・い空」「―・いものをもっと食べる必要がある」
            〔「あおい空（海）」は「碧い」とも書く〕
            （２）赤みが足りない。青ざめている。「―・い月」「―・い顔」
            （３）〔未熟の果実が青いことから〕
            修行・知識などが不十分だ。まだ一人前でない。「まだ考えが―・い」
            [派生] ――さ（名）――み（名）
            [慣用] 尻が―/風青し
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あおき-しゅうすけ</HEAD> アヲキシウスケ 【青木周弼】
            <INDENT=4>(1803-1863)
            〔名は「しゅうひつ」とも〕
            江戸末期の蘭方医。周防(スオウ)の人。名は邦彦。長州藩医となり，藩内で種痘を実施した。著「察病論」「病理論」など。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>ぎょ-ちょう</HEAD> ―テウ 【魚鳥】
            <INDENT=4>（１） [3][0]
            目じりが上に上がった目。
            （２） [0]
            価格などが上がる傾向にあること。上がり始め。
            <LINK>⇔下がり目</LINK[144847:1932]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あかじ-ざいせい</HEAD> [4] 【赤字財政】
            <INDENT=4>公債の発行や借入金によって（公債元本の償還費を除く）歳出をまかなっている財政。
            ⇔健全財政
            ⇔均衡財政
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あか・す</HEAD> [2] 【飽かす】
            <INDENT=4>■一■ （動サ五［四］）
            〔下一段動詞「飽かせる」の五段化〕
            （１）飽きさせる。「人を―・さない」
            （２）満足するまで十分使う。「金に―・して建てた家」「暇に―・す」
            ■二■ （動サ下二）
            <LINK>⇒あかせる</LINK[137903:2016]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あから-け・し</HEAD> 【赤らけし】 （形ク）
            <INDENT=4>赤みを帯びている。
            〔用例は「あからけみ」の形しか見られない〕
            <LINK>→赤らけみ</LINK[137924:2022]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>おお-おおじ</HEAD> オホオホヂ 【大祖父】
            <INDENT=4>祖父母の父。曾祖父(ソウソフ)。ひいじじ。ひじじ。
            <LINK>⇔大祖母(オオオバ)</LINK[140007:892]>
            ［和名抄］
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アルト</HEAD> [1] 〖(イタリア) alto〗
            <INDENT=4>〔音〕
            〔「高い」の意。テノールより高いところから〕
            （１）低い音域の女声。また，その音域の声部や歌手。
            （２）多く管楽器で，アルトの音域の楽器。アルト-サクソフォーンなど。また，特にフランスでビオラの別名。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>たん-じゅん</HEAD> [0] 【単純】 （名・形動）[文]ナリ
            <INDENT=4>（１）（ア）こみいった点がなく簡単な・こと（さま）。
            <LINK>⇔複雑</LINK[153396:12]>
            「―な構造」「―なミス」（イ）考え方などが一面的で行き届かない・こと（さま）。「―な発想」「―な頭の働き」
            （２）他種のものがまざっていない・こと（さま）。純一。「―泉(セン)」「彼女の意味する通りの―さで津田の耳へは響かなかつた/明暗（漱石）」
            （３）制限や条件のない・こと（さま）。「―承認」
            [派生] ――さ（名）
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>び-わ</HEAD> ―ハ [1] 【枇杷】
            <INDENT=4>バラ科の常緑高木。西日本に自生し，また中国から果樹として渡来した。葉は長楕円形で革質。初冬，枝頂に白色の小花を多数つける。果実は卵球形で大きな種子が数個あり，初夏，橙黄色に熟する。果実を食用，葉を薬用とし，材は櫛(クシ)や木刀を作る。[季]夏。
            〔「枇杷の花」は [季]冬〕
            《―を食むぽろり＼／と種二つ/星野立子》
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>いっ-ぱん</HEAD> [0] 【一般】 （名・形動）[文]ナリ
            <INDENT=4>（１）いろいろの事物・場合に広く認められ，成り立つこと。特別でないこと。普遍。
            <LINK>⇔特殊</LINK[150597:282]>
            （ア）普通であること。通常。「―の家庭」（イ）普通の人々。世間。「―に公開する」「―の受付を始める」（ウ）基本的・概括的なこと。全般にわたること。「―教養」「―論」
            （２）同一であること。同様であること。「恰も兵士が検閲式に列する時と―なり/八十日間世界一周（忠之助）」
            〔（１）は明治以後の用法〕
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>アルマン</HEAD> 〖Arman〗
            <INDENT=4>(1928-　)
            〔本名 Armand Fernandez〕
            フランスの画家・彫刻家。日用品の廃棄物を圧縮し，プレクシグラスの箱に詰め込んだ作品で知られる。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>エックハルト</HEAD> 〖Johannes Eckhart〗
            <INDENT=4>(1260頃-1327)
            〔一般に Meister Eckhart と呼ばれる〕
            ドイツの神秘主義者。ドミニコ会士。説教者として活躍。「存在は神である」との言葉を残し，人は神のうちに生き存在していると説いた。汎神論的として異端とされたが，のちの神秘主義に重大な影響を与えた。著「神の慰めの書」など。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>エロチシズム</HEAD> [4] 〖eroticism〗
            <INDENT=4>〔エロティシズムとも〕〔愛の神エロスに基づく。本来は精神的な愛を意味する〕
            （１）愛欲的・性欲的であること。好色的。色情的。「―を感じさせる踊り」
            （２）芸術作品で，性的なものをテーマにしていること。官能的であること。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>おおきな</HEAD> オホキナ [1] 【大きな】 （形動）
            <INDENT=4>〔形容動詞「おおき（なり）」の連体形から。現代語では連体形「おおきな」の形だけが用いられる〕
            大きい。たいへんな。
            <LINK>⇔小さな</LINK[149143:1134]>
            「―山」「規模の―会社」
            〔「おおきな」を連体詞とする説もあるが，この語は「耳の大きな人」などのように，述語としてのはたらきをもっている点が，一般の連体詞とは異なっている〕
            <LINK>→おおき</LINK[140014:150]>
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>こ・い</HEAD> [1] 【濃い】 （形）[文]ク こ・し
            <INDENT=4>（１）物の濃度・密度が大きい。
            <LINK>⇔薄い</LINK[139310:1084]>
            （ア）色が深い。
            <LINK>⇔淡い</LINK[138426:18]>
            「―・い緑」「夕闇が―・い」（イ）味・匂い・化粧などが強い。
            <LINK>⇔淡い</LINK[138426:18]>
            「―・い味つけにする」「ジャスミンの―・い香り」「おしろいが―・い」（ウ）生えているものの密度が高い。「―・いひげ」「髪の毛が―・い」（エ）液状のものについて，溶けている物質の水に対する割合が大きい。「小麦粉を―・くとく」「―・い粥(カユ)」（オ）霧やもやなどの濃度が大きい。「―・いもや」「ガスが―・く立ち込める」
            （２）物事の程度が強い。（ア）何かの様子が強く表れている。「疲労の色が―・い」「敗色が―・い」（イ）可能性の度合が大きい。「犯罪の疑いが―・い」（ウ）情愛が濃厚である。「情が―・い」
            （３）特に，紅色・紫色が深い。「かのしるしの扇は，桜の三重がさねにて，―・き方に，霞める月を書きて/源氏（花宴）」
            （４）人間関係が密接である。交わりが深い。「などてかくはひあひがたき紫を心に深く思ひそめけむ，―・くなりはつまじきにや/源氏（真木柱）」
            [派生] ――さ（名）
            [慣用] 血は水よりも―
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>グレード-アップ</HEAD> [5]
            <INDENT=4>〔和 grade＋up〕 （名）スル
            等級・品質を上げること。格上げ。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>てん-い</HEAD> [1] 【転移】 （名）スル
            <INDENT=4>（１）場所などをうつすこと。また，うつること。移転。「備州小田郡笠岡へ―せられ/新聞雑誌 50」
            （２）移りかわること。「好みは時代とともに―する」
            （３）〔医〕 腫瘍(シユヨウ)細胞や病原体が血流やリンパ流に入り，他の場所に移行・定着して，原発巣と同一の変化を起こすこと。
            （４）〔transition〕
            物質が一つの状態から他の状態に変化すること。気相・液相・固相間の相転移，同一物質の異なる結晶形の間での多形転移，同素体の間での転移など。
            （５）〔心〕（ア）
            〔transfer〕
            前に行なった学習が，あとの学習効果に影響を与えること。あとの学習を促進する場合を正の転移，妨害・抑制する場合を負の転移という。学習転移。（イ）
            〔transference〕
            精神分析で，患者が過去に親など重要な人物に向けたのと同じ感情や態度を治療者に向けること。
            """),

            dedent(u"""\
            <INDENT=1><PAGE><HEAD>ほう</HEAD> [0] 【法】
            <INDENT=4>□一□〔歴史的仮名遣い「はふ」〕
            （１）物事に秩序を与えているもの。法則。のり。「―にかなった振る舞い」
            （２）社会生活を維持し統制するために，強制力をもって行われる社会規範。法律。「―の裁き」「―を犯す」
            （３）やり方。しかた。方法。「無事助け出す―はないものか」「客を放っておくという―があるものか」
            （４）〔mood〕
            インド-ヨーロッパ語で，表現内容に対する話し手の心的態度を表す動詞の語形変化。直説法・命令法・接続法（仮定法）などに分かれる。
            □二□〔歴史的仮名遣い「ほふ」〕
            〔仏〕
            〔梵 dharma「達磨」などと音訳〕
            （１）事物。物。存在。「諸―無我」
            （２）（ア）真理。根本的な規範。（イ）教え。教説。教義。（ウ）仏の教え。釈迦の言葉。それを記録した経。（エ）教義・信者・教団などによって具体化されている仏教。（オ）仏事・法要・祈祷などの儀式。「祈雨の―」
            """),
        ]

        for body in test_entries:
            print body
            d = (ENTRY_BLOCK + stringEnd).parseString(body).dump()
            pp.pprint(d)
            print

    def test_multi_entries(self):
        test_bodies = [
            dedent(u"""\
            <INDENT=1><PAGE><HEAD>あ</HEAD>
            <INDENT=4>（１）五十音図ア行第一段の仮名。後舌の広母音。
            （２）平仮名「あ」は「安」の草体。片仮名「ア」は「阿」の行書体の偏。
            <INDENT=1><PAGE><HEAD>あ</HEAD> 【足】
            <INDENT=4>あし。「―の音せず行かむ駒もが/万葉 3387」
            〔多く「足掻(アガ)き」「足結(アユイ)」など，複合した形で見られる〕
            """),
        ]
        for text in test_bodies:
            print text
            f = StringIO(text)
            entry_buffer = list()
            for line in f:
                is_entry_header = ENTRY_HEADER_MATCHER.match(line)
                if is_entry_header and entry_buffer:
                    entry_lines = ''.join(entry_buffer)
                    print entry_lines
                    
                    d = (ENTRY_BLOCK + stringEnd).parseString(entry_lines).dump()
                    pp.pprint(d)
                    print

                    entry_buffer = list()
                entry_buffer.append(line)
            entry_lines = ''.join(entry_buffer)
            print entry_lines

            d = (ENTRY_BLOCK + stringEnd).parseString(entry_lines).dump()
            pp.pprint(d)
            print

    def test_definition_blocks(self):
        test_blocks = [
            dedent(u"""\
            五十音図ア行第一段の仮名。後舌の広母音。
            """),

            dedent(u"""\
            あし。「―の音せず行かむ駒もが/万葉 3387」
            """),

            dedent(u"""\
            話した内容や心の中で考えたことがらなどをさす。「―でもないこうでもない」「―言っておいたから，大丈夫だろう」
            """),

            dedent(u"""\
            イギリスの詩人。釈迦の生涯・教義を長編無韻詩「アジアの光」に著した。
            """),

            dedent(u"""\
            イギリスの詩人・批評家。文明批評にまで発展させた「教養と無秩序」のほか，「批評論集」などの著がある。
            """),

            dedent(u"""\
            「ようす」「ぐあい」などの意を表す。「色―」「肌―」
            """),

            dedent(u"""\
            対象をかけがえのないものと認め，それに引き付けられる心の動き。また，その気持ちの表れ。（ア）相手をいつくしむ心。相手のために良かれと願う心。「子への―」「―を注ぐ」「―の手をさしのべる」（イ）異性に対して抱く思慕の情。恋。「―が芽生える」「―を告げる」「―をはぐくむ」（ウ）何事にもまして，大切にしたいと思う気持ち。「学問に対する―」
            """),

            dedent(u"""\
            名詞に付いて，「同じ」という意を表す。「―弟子」「―部屋」
            """),

            dedent(u"""\
            活用語の連体形に付いて，接続助詞のように用いる。記録体・和漢混交文に多く用いられた。（ア）単に前の叙述を後の叙述に続ける。ところ。「鹿を射むと思て待ち立てりし―，俄(ニワカ)に虎来て喰らはんとせし時/今昔 1」（イ）前の叙述が後の叙述の理由・原因であることを表す。ゆえに。「後に，さかしき人々書きいれたる―，物語多くなれり/宇治拾遺（序）」
            """),

            dedent(u"""\
            「―な構造」「―なミス」（イ）考え方などが一面的で行き届かない・こと（さま）。「―な発想」「―な頭の働き」
            """),

            dedent(u"""\
            「―・い緑」「夕闇が―・い」（イ）味・匂い・化粧などが強い。
            """),

            dedent(u"""\
            「―・い味つけにする」「ジャスミンの―・い香り」「おしろいが―・い」（ウ）生えているものの密度が高い。「―・いひげ」「髪の毛が―・い」（エ）液状のものについて，溶けている物質の水に対する割合が大きい。「小麦粉を―・くとく」「―・い粥(カユ)」（オ）霧やもやなどの濃度が大きい。「―・いもや」「ガスが―・く立ち込める」
            """),

            dedent(u"""\
            物事の程度が強い。（ア）何かの様子が強く表れている。「疲労の色が―・い」「敗色が―・い」（イ）可能性の度合が大きい。「犯罪の疑いが―・い」（ウ）情愛が濃厚である。「情が―・い」
            """),

            dedent(u"""\
            （ア）ユズの葉。きのめ。（イ）茶。
            """),

            dedent(u"""\
            浄瑠璃用語。（ア）
            """),

            dedent(u"""\
            （イ）
            """),

            dedent(u"""\
            （２）〔文法〕「相(ソウ){（３）（ア）}」に同じ。
            """),

            dedent(u"""\
            <LINK>→あたう（能）(１)（イ）</LINK[138113:656]>
            """),

            dedent(u"""\
            <LINK>→アルコール(１)（ア）[表]</LINK[177020:224]>
            """),

            dedent(u"""\
            <FIG>釜（１）（ア）</FIG>[図]
            """),

            dedent(u"""\
            〔（ア）は明治以降，英語の he などの訳語として生じたものであるが，日本語では同輩以下のものをさすのが普通〕
            """),

            dedent(u"""\
            あし。「―の音せず行かむ駒もが/万葉 3387」
            〔多く「足掻(アガ)き」「足結(アユイ)」など，複合した形で見られる〕
            """),

            dedent(u"""\
            いろいろの事物・場合に広く認められ，成り立つこと。特別でないこと。普遍。
            <LINK>⇔特殊</LINK[150597:282]>
            （ア）普通であること。通常。「―の家庭」（イ）普通の人々。世間。「―に公開する」「―の受付を始める」（ウ）基本的・概括的なこと。全般にわたること。「―教養」「―論」
            """),
        ]

        for block in test_blocks:
            print '---'
            # print block
            e = ESCAPE_EMBEDDED_SUBDEFINITIONS.transformString(block)
            print e
            d = (SUBDEFINITION_BLOCK + stringEnd).parseString(e).dump()
            pp.pprint(d)
            print


if __name__ == '__main__':
    unittest.main()
