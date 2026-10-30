from pathlib import Path

p = Path("project/app/src/main/java/br/com/aventuraelemental/MainActivity.kt")
s = p.read_text(encoding="utf-8")

def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: esperado 1 trecho, encontrado {n}")
    s = s.replace(old, new, 1)

# O mapa ganha uma vila mais viva, com casas secundárias e animais visíveis.
rep('''            drawImage(houseSheet, IntOffset(32, 112), IntSize(96, 112), IntOffset(houseX, (ch * .05f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * 4.2f).toInt()))
''',
'''            drawImage(houseSheet, IntOffset(32, 112), IntSize(96, 112), IntOffset(houseX, (ch * .05f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * 4.2f).toInt()))
            if (area == 0) {
                drawImage(houseSheet, IntOffset(0, 0), IntSize(64, 64),
                    IntOffset((cw * .35f).toInt(), (ch * .15f).toInt()), IntSize((cw * 2.1f).toInt(), (ch * 2.1f).toInt()))
                drawImage(houseSheet, IntOffset(64, 0), IntSize(64, 64),
                    IntOffset((cw * 6.25f).toInt(), (ch * 5.2f).toInt()), IntSize((cw * 2.1f).toInt(), (ch * 2.1f).toInt()))
            }
''', "casas adicionais")

rep('''            val decorSheet = remember { context.assets.open("clover_valley/Enviroment/Decor/Natural_Decor_free.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }
''',
'''            val decorSheet = remember { context.assets.open("clover_valley/Enviroment/Decor/Natural_Decor_free.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }
''', "decor existente") if False else None

# Acrescenta animais animados ao mapa como habitantes da vila.
rep('''    val fenceSheet = remember { context.assets.open("clover_valley/Tilesets/Fences.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }

    Column''',
'''    val fenceSheet = remember { context.assets.open("clover_valley/Tilesets/Fences.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }
    val pigSheet = remember { context.assets.open("clover_valley/Animals/Pig/Pig-Sheet.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }
    val sheepSheet = remember { context.assets.open("clover_valley/Animals/Sheep/Sheep-Sheet.png").use { BitmapFactory.decodeStream(it).asImageBitmap() } }

    Column''', "sprites dos animais")

rep('''        Canvas(Modifier.fillMaxWidth().height(310.dp)) {''',
'''        Canvas(Modifier.fillMaxWidth().height(350.dp)) {''', "mapa maior")

rep('''            // Personagem original, com orientação correta e espelhamento lateral.
            val spriteSize = (minOf(cw, ch) * 1.75f).toInt().coerceAtLeast(1)
''',
'''            // Pequenos habitantes animados dão vida à vila.
            val animalSize = (minOf(cw, ch) * 1.45f).toInt().coerceAtLeast(1)
            drawImage(pigSheet, IntOffset(0, 0), IntSize(64, 64),
                IntOffset((cw * 1.25f).toInt(), (ch * 6.4f).toInt()), IntSize(animalSize, animalSize))
            drawImage(sheepSheet, IntOffset(0, 0), IntSize(64, 64),
                IntOffset((cw * 7.1f).toInt(), (ch * 7.0f).toInt()), IntSize(animalSize, animalSize))

            // Personagem original, com orientação correta e espelhamento lateral.
            val spriteSize = (minOf(cw, ch) * 1.9f).toInt().coerceAtLeast(1)
''', "habitantes no mapa")

# Batalhas passam a usar três artes diferentes do pacote, em vez do mesmo slime recolorido.
start = s.index("@Composable\nfun CreatureArt(")
end = s.index("\n@Composable\nfun HpBar", start)
new_func = '''@Composable
fun CreatureArt(color: Color, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val isFire = color == Color(0xFFFF855E)
    val isWater = color == Color(0xFF69C7FF)
    val spritePath = when {
        isFire -> "clover_valley/Animals/Pig/Pig-Sheet.png"
        isWater -> "clover_valley/Animals/Sheep/Sheep-Sheet.png"
        else -> "clover_valley/Enemies/Slime/Slime-Idle-Sheet.png"
    }
    val frameCount = if (isFire || isWater) 6 else 3
    var frame by remember(spritePath) { mutableIntStateOf(0) }
    LaunchedEffect(spritePath) {
        while (true) {
            delay(220)
            frame = (frame + 1) % frameCount
        }
    }
    val sprite = remember(spritePath) {
        runCatching {
            context.assets.open(spritePath).use { BitmapFactory.decodeStream(it).asImageBitmap() }
        }.getOrNull()
    }
    Canvas(modifier) {
        val side = minOf(size.width, size.height).toInt().coerceAtLeast(1)
        drawOval(Color(0x55000000), Offset(size.width * .2f, size.height * .82f),
            Size(size.width * .6f, size.height * .1f))
        if (sprite != null) {
            drawImage(
                image = sprite,
                srcOffset = IntOffset(frame * 64, 0),
                srcSize = IntSize(64, 64),
                dstOffset = IntOffset(((size.width - side) / 2).toInt(), ((size.height - side) / 2).toInt()),
                dstSize = IntSize(side, side),
                colorFilter = if (isFire || isWater) null else ColorFilter.tint(color)
            )
        }
    }
}
'''
s = s[:start] + new_func + s[end:]

# Campo de batalha com cenário verde, mantendo painéis de status legíveis.
rep('''            "battle" -> Column(Modifier.fillMaxSize().padding(18.dp)) {''',
'''            "battle" -> Column(Modifier.fillMaxSize().background(Color(0xFF477D55)).padding(14.dp)) {''', "campo de batalha")

# Aparência de aventura no menu: moldura de pixel-art e personagem real do pacote.
rep('''            "home" -> Column(
                Modifier.fillMaxSize().padding(22.dp),''',
'''            "home" -> Column(
                Modifier.fillMaxSize().background(Color(0xFF203D52)).padding(22.dp),''', "menu com identidade")
rep('''                Text("AVENTURA", color = Mint, fontSize = 16.sp, fontWeight = FontWeight.Black, letterSpacing = 5.sp)
                Text("ELEMENTAL", color = Paper, fontSize = 38.sp, fontWeight = FontWeight.Black)''',
'''                Text("AVENTURA", color = Gold, fontSize = 17.sp, fontWeight = FontWeight.Black, letterSpacing = 5.sp)
                Text("ELEMENTAL", color = Paper, fontSize = 38.sp, fontWeight = FontWeight.Black)
                Text("CAPTURE  •  TREINE  •  EVOLUA", color = Mint, fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)''', "marca do jogo")

p.write_text(s, encoding="utf-8")
print("Visual refresh applied")
