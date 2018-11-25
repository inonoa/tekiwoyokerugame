import objects
import pygame
import screen

class Scene():
    def __init__(self,):
        self.lyrs = [[],[],[],[],[],[],[],[],[],[]] # 0~9の10レイヤー(まあ十分やろ知らんけど),この順で処理(衝突とかは別かなあ)する
        # こっちが低レイヤー
        # 
        #
        # phantom
        #
        #
        # boss
        # 
        # enemy
        #
        # UI
        # こっちが高レイヤー
        self.enms = [] # 当たり判定するやつ

        self.isEnd = False
        self.nextScnNum = 0
        self.nextScns = []
        self.havePause = False
    
    def makeNextScene(self,):
        pass

class TitleScene(Scene):
    def __init__(self,):
        super().__init__()
        titleBG = objects.GameObject(objects.titleBGImgGrp,self,0,[-10,-10])
        titleUI = objects.TitleUI(self)
    
    def makeNextScene(self,):
        gameScene = GameScene()
        self.nextScns = [gameScene]

class GameScene(Scene):
    def __init__(self,):
        super().__init__()

        self.havePause = True
        background = objects.GameObject(objects.bgImgGrp,self,0,(-106,0))
        hero = objects.Hero(self)
        hpgauge = objects.HPGauge(hero,objects.HPImgGrp,self)
        enemySpawner = objects.EnemySpawner(self,hero)

    def makeNextScene(self,):
        gameOverScene = GameOverScene()
        resultSnene = ResultScene()
        self.nextScns = [gameOverScene,resultSnene]

class GameOverScene(Scene):
    def __init__(self,):
        super().__init__()
        gameoverImg = pygame.display.get_surface().copy()
        goBGimgGrp = objects.ImageGroup([gameoverImg],screen.screen)
        gameoverBG = objects.GameObject(goBGimgGrp,self,0,(0,0))
        gameoverObj = objects.GameObject(objects.gmovImgGrp,self,1,(-10,-10))
        gameRestarter = objects.GameRestarter(self)

    def makeNextScene(self,):
        titleScene = TitleScene()
        self.nextScns = [titleScene]

class ResultScene(Scene):
    def __init__(self,):
        super().__init__()
        resultBGObj = objects.GameObject(objects.resultBGImgGrp,self,0,[-10,-10])
        clearObj = objects.ClearObj(self)
        comet = objects.Comet(self)
        clearObj.cmt = comet
        comet.clrobj = clearObj
    
    def makeNextScene(self,):
        titleScene = TitleScene()
        self.nextScns = [titleScene]