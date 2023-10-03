import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

# こうかとんの移動量(上下左右)
delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}


def check_bound(obj_rct): # はみ出しチェック
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル（横、縦方向判定結果）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向
        tate = False
    return yoko, tate

def d(dic1,dic2):
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_r_img = pg.transform.flip(kk_img,True,False)
    t = (dic1,dic2)
    print(t)
    dilec = {
        (0,0):pg.transform.rotozoom(kk_img, 0, 2.0),
        (0,-5):pg.transform.rotozoom(kk_r_img, 90, 2.0),
        (+5,-5):pg.transform.rotozoom(kk_r_img, 45, 2.0),
        (+5,0):pg.transform.rotozoom(kk_r_img, 0, 2.0),
        (+5,+5):pg.transform.rotozoom(kk_r_img, -45, 2.0),
        (0,+5):pg.transform.rotozoom(kk_r_img, -90, 2.0),
        (-5,+5):pg.transform.rotozoom(kk_img, 45, 2.0),
        (-5,0):pg.transform.rotozoom(kk_img, 0, 2.0),
        (-5,-5):pg.transform.rotozoom(kk_img, -45, 2.0)
    }
    for key, vl in dilec.items():
        if t == key:
            print(dilec[key])
            return vl
        
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    # kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = d(0,0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)

    """爆弾"""
    bomb_img = pg.Surface((20, 20)) # 爆弾surface
    bomb_img.set_colorkey((0,0,0))
    pg.draw.circle(bomb_img, (255,0,0), (10,10) ,10)
    bomb_rct = bomb_img.get_rect() # surfaceからrect抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bomb_rct.center = (x, y) # rectにランダムな座標設定
    vx, vy = +5, +5 #爆弾座標を+5ずつ動かす

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        # 衝突判定
        if kk_rct.colliderect(bomb_rct): # もし重なったら
            print("Game Over")
            return # main関数から抜ける

        """こうかとん"""
        screen.blit(bg_img, [0, 0])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0] # 合計移動量
        for key, mv in delta.items(): # 辞書の取得
            if key_lst[key]:
                sum_mv[0] += mv[0] # 横方向
                sum_mv[1] += mv[1] # 縦方向
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) # 指定の画像を変数ずつ動かす
        if check_bound(kk_rct) != (True, True): # はみ出し判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])


        kk_img = d(sum_mv[0],sum_mv[1])
        screen.blit(kk_img, kk_rct)        
        
        """爆弾"""
        bomb_rct.move_ip(vx,vy) # 指定の画像を変数ずつ動かす
        yoko, tate = check_bound(bomb_rct)
        if not yoko: # 符号反転によるはみ出し判定
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bomb_img, bomb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()