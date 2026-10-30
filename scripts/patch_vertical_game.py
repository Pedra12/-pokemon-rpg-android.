from pathlib import Path

game = Path("project/app/src/main/java/br/com/aventuraelemental/MainActivity.kt")
src = game.read_text(encoding="utf-8")

def rep(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one match, found {n}")
    src = src.replace(old, new, 1)

rep("import androidx.compose.foundation.Canvas\n",
    "import androidx.compose.foundation.Canvas\nimport androidx.compose.foundation.gestures.detectDragGestures\n", "drag import")
rep("import androidx.compose.ui.platform.LocalContext\n",
    "import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.ui.input.pointer.pointerInput\n", "pointer import")
rep("import kotlin.random.Random\n",
    "import kotlin.random.Random\nimport kotlin.math.abs\n", "abs import")

rep('    var player = remember { Creature("Brasa", "FOGO", 44, 10, Color(0xFFFF855E)) }\n',
    '    var player = remember { Creature("Brasa", "FOGO", 44, 10, Color(0xFFFF855E)) }\n'
    '    var evolved by remember { mutableStateOf(prefs.getBoolean("evolved", false)) }\n'
    '    val playerName = if (evolved) "Brasalume" else "Brasa"\n'
    '    val playerMaxHp = if (evolved) 56 else 44\n'
    '    var capturedCreatures by remember { mutableStateOf(prefs.getString("captured", "") ?: "") }\n'
    '    var storyStage by remember { mutableIntStateOf(prefs.getInt("storyStage", 0)) }\n',
    "progression state")
rep('    var playerHp by remember { mutableIntStateOf(prefs.getInt("hp", 44).coerceIn(1, 44)) }\n',
    '    var playerHp by remember { mutableIntStateOf(prefs.getInt("hp", playerMaxHp).coerceIn(1, playerMaxHp)) }\n',
    "player max hp")
rep('            .putInt("level", level).putInt("xp", xp).putString("facing", facing).apply()\n',
    '            .putInt("level", level).putInt("xp", xp).putString("facing", facing)\n'
    '            .putString("captured", capturedCreatures).putBoolean("evolved", evolved)\n'
    '            .putInt("storyStage", storyStage).apply()\n',
    "save collection")

helpers = """    fun awardVictory(amount: Int) {
        wins++
        xp += amount
        if (xp >= level * 25) {
            xp -= level * 25
            level++
            if (level >= 5 && !evolved) {
                evolved = true
                playerHp = (playerHp + 12).coerceAtMost(56)
                message = "Brasa evoluiu para Brasalume!"
            } else {
                message = "$enemyName caiu! Você subiu para o nível $level!"
            }
        } else {
            message = "$enemyName caiu! +$amount XP."
        }
        playerHp = (playerHp + 8).coerceAtMost(if (evolved) 56 else 44)
        battleResolved = true
        save()
    }

    fun captureCreature() {
        if (battleResolved) return
        val chance = (28 + (enemyMaxHp - enemyHp) * 62 / enemyMaxHp.coerceAtLeast(1)).coerceIn(25, 90)
        if (Random.nextInt(100) < chance) {
            val current = capturedCreatures.split("|").filter { it.isNotBlank() }
            val duplicate = current.contains(enemyName)
            if (!duplicate) capturedCreatures = (current + enemyName).joinToString("|")
            battleResolved = true
            message = if (duplicate) "$enemyName já está registrado na sua equipe."
                else "$enemyName foi capturado e entrou para sua equipe!"
            save()
        } else {
            message = "$enemyName escapou da esfera!"
            playerHp = (playerHp - enemyAttack).coerceAtLeast(0)
            if (playerHp <= 0) {
                playerHp = (if (evolved) 56 else 44) / 2
                message += " $playerName recuperou parte da vida."
            }
            save()
        }
    }

    fun movePlayer(dx: Int, dy: Int) {"""
rep("    fun movePlayer(dx: Int, dy: Int) {", helpers, "capture and evolution logic")

rep("""        playerX = nx
        playerY = ny
        steps++
        message = listOf("O vento balança as folhas.", "Você ouve algo na grama.", "A trilha continua adiante.").random()
""",
"""        playerX = nx
        playerY = ny
        steps++
        message = listOf("O vento balança as folhas.", "Você ouve algo na grama.", "A trilha continua adiante.").random()
        if (nx == 4 && ny == 6 && storyStage == 0) {
            storyStage = 1
            message = "Lívia: As criaturas estão inquietas. O coração do Vale está perdendo sua luz."
        } else if (nx == 7 && ny == 7 && storyStage == 1 && wins >= 2) {
            storyStage = 2
            message = "Guardião do Vale: Fortaleça sua equipe. O caminho para o Lago Azul está quase aberto."
        }
""", "story dialogue")

rep('                    TextButton(onClick = { save(); screen = "home" }) { Text("MENU", color = Gold) }\n',
    '                    TextButton(onClick = { screen = "team" }) {\n'
    '                        Text("EQUIPE (${1 + capturedCreatures.split("|").count { it.isNotBlank() }})", color = Gold)\n'
    '                    }\n'
    '                    TextButton(onClick = { save(); screen = "home" }) { Text("MENU", color = Gold) }\n',
    "team button")
rep("                WorldMap(playerX, playerY, facing, steps)\n",
    "                WorldMap(playerX, playerY, facing, steps) { dx, dy -> movePlayer(dx, dy) }\n",
    "map movement callback")
rep('                        Text("Treinador Nv. $level  •  $xp XP", color = Paper, fontSize = 13.sp)\n',
    '                        Text("$playerName  Nv. $level  •  $xp XP", color = Paper, fontSize = 13.sp)\n',
    "player display")
rep('                    StatCard("VIDA", "$playerHp/44", Modifier.weight(1f))\n',
    '                    StatCard("CRIATURAS", "${1 + capturedCreatures.split("|").count { it.isNotBlank() }}", Modifier.weight(1f))\n',
    "collection counter")

rep("""                                battleResolved = true
                                wins++; xp += 12
                                if (xp >= level * 25) { xp -= level * 25; level++; message = "$enemyName caiu! Você subiu para o nível $level!" }
                                else message = "$enemyName caiu! +12 XP."
                                playerHp = (playerHp + 8).coerceAtMost(44)
                                save()
""", "                                awardVictory(12)\n", "fire victory")
rep("""                                battleResolved = true
                                wins++; xp += 10; playerHp = (playerHp + 6).coerceAtMost(44)
                                if (xp >= level * 25) { xp -= level * 25; level++; message = "Vitória! Você subiu para o nível $level!" } else message = "Vitória! +10 XP."
                                save()
""", "                                awardVictory(10)\n", "normal victory")

src = src.replace('Text("Brasa  Nv.$level"', 'Text("$playerName  Nv.$level"')
src = src.replace('Text("$playerHp / 44 PV"', 'Text("$playerHp / $playerMaxHp PV"')
src = src.replace('HpBar(playerHp, 44)', 'HpBar(playerHp, playerMaxHp)')
src = src.replace('playerHp < 44', 'playerHp < playerMaxHp')
src = src.replace('coerceAtMost(44)', 'coerceAtMost(playerMaxHp)')
src = src.replace('Brasa usou Faísca!', '$playerName usou Faísca!')
src = src.replace('Brasa avançou!', '$playerName avançou!')
src = src.replace('Brasa usou uma poção.', '$playerName usou uma poção.')

rep("""                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(
                        enabled = !battleResolved && potions > 0 && playerHp < playerMaxHp,
""",
"""                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    OutlinedButton(
                        enabled = !battleResolved,
                        onClick = { captureCreature() },
                        modifier = Modifier.weight(1f)
                    ) { Text("Capturar", color = Mint, fontSize = 11.sp) }
                    OutlinedButton(
                        enabled = !battleResolved && potions > 0 && playerHp < playerMaxHp,
""", "capture action button")
rep('                    ) { Text("Poção +14 ($potions)", color = Mint) }\n'
    '                    OutlinedButton(enabled = !battleResolved, onClick = { screen = "world"; message = "Você saiu do encontro."; save() }, modifier = Modifier.weight(1f)) { Text("Fugir", color = Paper) }\n',
    '                    ) { Text("Poção +14 ($potions)", color = Mint, fontSize = 11.sp) }\n'
    '                    OutlinedButton(enabled = !battleResolved, onClick = { screen = "world"; message = "Você saiu do encontro."; save() }, modifier = Modifier.weight(1f)) { Text("Fugir", color = Paper, fontSize = 11.sp) }\n',
    "compact battle actions")

rep("            else -> Unit\n",
"""            "team" -> Column(
                Modifier.fillMaxSize().padding(20.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text("SUA EQUIPE", color = Mint, fontWeight = FontWeight.Black, letterSpacing = 3.sp, fontSize = 22.sp)
                Spacer(Modifier.height(18.dp))
                Text("$playerName  •  FOGO  •  Nv. $level", color = Paper, fontWeight = FontWeight.Bold)
                Text("Vida: $playerHp / $playerMaxHp", color = Gold)
                Spacer(Modifier.height(18.dp))
                Text("CRIATURAS CAPTURADAS", color = Mint, fontWeight = FontWeight.Bold)
                val owned = capturedCreatures.split("|").filter { it.isNotBlank() }
                if (owned.isEmpty()) {
                    Text("Sua equipe ainda está começando. Capture criaturas durante os encontros.", color = Color.LightGray, textAlign = TextAlign.Center)
                } else {
                    owned.forEachIndexed { index, name ->
                        Text("${index + 1}. $name", color = Paper, modifier = Modifier.fillMaxWidth().padding(vertical = 5.dp))
                    }
                }
                Spacer(Modifier.height(22.dp))
                BigButton("VOLTAR AO MAPA") { screen = "world" }
            }
            else -> Unit
""", "team screen")

rep("fun WorldMap(px: Int, py: Int, facing: String, stepCount: Int) {",
    "fun WorldMap(px: Int, py: Int, facing: String, stepCount: Int, onMove: (Int, Int) -> Unit) {",
    "map function signature")
rep("        Canvas(Modifier.fillMaxWidth().height(310.dp)) {",
"""        Canvas(
            Modifier.fillMaxWidth().height(310.dp).pointerInput(onMove) {
                var dragTotal = Offset.Zero
                detectDragGestures(
                    onDragEnd = {
                        if (abs(dragTotal.x) > abs(dragTotal.y) && abs(dragTotal.x) > 22f) {
                            onMove(if (dragTotal.x > 0) 1 else -1, 0)
                        } else if (abs(dragTotal.y) > 22f) {
                            onMove(0, if (dragTotal.y > 0) 1 else -1)
                        }
                        dragTotal = Offset.Zero
                    },
                    onDragCancel = { dragTotal = Offset.Zero }
                ) { change, dragAmount ->
                    change.consume()
                    dragTotal += dragAmount
                }
            }
        ) {""", "drag movement")


# Replace placeholder vector monsters with the supplied pixel-art slime sprites.
rep("import androidx.compose.ui.graphics.Color\n",
    "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.ColorFilter\n", "pixel-art color filter import")

rep("    var anim by remember { mutableIntStateOf(0) }\n",
    "    var anim by remember { mutableIntStateOf(0) }\n    var attackFrame by remember { mutableIntStateOf(-1) }\n", "attack animation state")
rep("    var battleResolved by remember { mutableStateOf(false) }\n",
    "    var battleResolved by remember { mutableStateOf(false) }\n"
    "    LaunchedEffect(anim) {\n"
    "        if (anim > 0) {\n"
    "            for (frame in 0..4) { attackFrame = frame; delay(45) }\n"
    "            attackFrame = -1\n"
    "        }\n"
    "    }\n", "attack animation effect")

rep('''                Text(message, color = Paper, modifier = Modifier.fillMaxWidth().background(Panel, RoundedCornerShape(12.dp)).padding(14.dp), textAlign = TextAlign.Center)
                Spacer(Modifier.height(16.dp))
''',
'''                Text(message, color = Paper, modifier = Modifier.fillMaxWidth().background(Panel, RoundedCornerShape(12.dp)).padding(14.dp), textAlign = TextAlign.Center)
                if (attackFrame >= 0) AttackBurst(attackFrame, Gold, Modifier.size(52.dp))
                Spacer(Modifier.height(16.dp))
''', "battle attack effect display")

old_creature = """@Composable
fun CreatureArt(color: Color, modifier: Modifier = Modifier) {
    Canvas(modifier) {
        val w = size.width; val h = size.height
        // sombra
        drawOval(Color(0x55000000), Offset(w*.18f,h*.78f), Size(w*.64f,h*.12f))
        // corpo e orelhas
        drawCircle(color, radius = w*.31f, center = Offset(w*.5f,h*.53f))
        drawCircle(color, radius = w*.15f, center = Offset(w*.28f,h*.28f))
        drawCircle(color, radius = w*.15f, center = Offset(w*.72f,h*.28f))
        drawCircle(Color(0xFF26364A), radius = w*.045f, center = Offset(w*.4f,h*.48f))
        drawCircle(Color(0xFF26364A), radius = w*.045f, center = Offset(w*.6f,h*.48f))
        drawArc(Color(0xFF26364A), 15f, 150f, false, Offset(w*.4f,h*.53f), Size(w*.2f,h*.13f), style = Stroke(width = w*.025f))
        drawCircle(Color.White, radius = w*.018f, center = Offset(w*.41f,h*.465f))
        drawCircle(Color.White, radius = w*.018f, center = Offset(w*.61f,h*.465f))
        // detalhe brilhante
        drawCircle(Color(0x99FFFFFF), radius = w*.07f, center = Offset(w*.35f,h*.37f))
    }
}
"""
new_creature = """@Composable
fun AttackBurst(frame: Int, color: Color, modifier: Modifier = Modifier) {
    Canvas(modifier) {
        val cx = size.width / 2f
        val cy = size.height / 2f
        val radius = size.minDimension * (0.16f + frame * 0.045f)
        val stroke = 2.dp.toPx()
        drawCircle(color, radius, Offset(cx, cy), style = Stroke(width = stroke))
        drawLine(color, Offset(cx - radius * 1.5f, cy), Offset(cx + radius * 1.5f, cy), strokeWidth = stroke)
        drawLine(color, Offset(cx, cy - radius * 1.5f), Offset(cx, cy + radius * 1.5f), strokeWidth = stroke)
        drawLine(color, Offset(cx - radius, cy - radius), Offset(cx + radius, cy + radius), strokeWidth = stroke)
        drawLine(color, Offset(cx + radius, cy - radius), Offset(cx - radius, cy + radius), strokeWidth = stroke)
    }
}

@Composable
fun CreatureArt(color: Color, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val slime = remember {
        runCatching {
            context.assets.open("clover_valley/Enemies/Slime/Slime-Idle-Sheet.png")
                .use { BitmapFactory.decodeStream(it).asImageBitmap() }
        }.getOrNull()
    }
    Canvas(modifier) {
        if (slime != null) {
            val side = minOf(size.width, size.height).toInt().coerceAtLeast(1)
            drawImage(
                image = slime,
                srcOffset = IntOffset(0, 0),
                srcSize = IntSize(64, 64),
                dstOffset = IntOffset(((size.width - side) / 2).toInt(), ((size.height - side) / 2).toInt()),
                dstSize = IntSize(side, side),
                colorFilter = ColorFilter.tint(color)
            )
        } else {
            drawCircle(color, radius = minOf(size.width, size.height) * .32f, center = Offset(size.width / 2, size.height / 2))
        }
    }
}
"""
rep(old_creature, new_creature, "pixel creatures and attack animation")


# Three connected regions unlock through victories and remain saved between sessions.
rep('    var storyStage by remember { mutableIntStateOf(prefs.getInt("storyStage", 0)) }\n',
    '    var storyStage by remember { mutableIntStateOf(prefs.getInt("storyStage", 0)) }\n'
    '    var area by remember { mutableIntStateOf(prefs.getInt("area", 0).coerceIn(0, 2)) }\n'
    '    var maxArea by remember { mutableIntStateOf(prefs.getInt("maxArea", 0).coerceIn(0, 2)) }\n'
    '    val areaName = listOf("VALE DAS FOLHAS", "LAGO AZUL", "BOSQUE ANTIGO")[area]\n',
    "region progression state")
rep('            .putInt("storyStage", storyStage).apply()\n',
    '            .putInt("storyStage", storyStage).putInt("area", area).putInt("maxArea", maxArea).apply()\n',
    "save regions")

c=c.replace(
    '        wins++\n        xp += amount\n',
    '        wins++\n        var unlockedAreaName: String? = null\n'
    '        if (wins >= 6 && maxArea < 2) { maxArea = 2; unlockedAreaName = "Bosque Antigo" }\n'
    '        else if (wins >= 3 && maxArea < 1) { maxArea = 1; unlockedAreaName = "Lago Azul" }\n'
    '        xp += amount\n',
    1
)
c=c.replace(
    '        battleResolved = true\n        save()\n    }\n\n    fun captureCreature()',
    '        if (unlockedAreaName != null) message = "Nova região liberada: $unlockedAreaName!"\n'
    '        battleResolved = true\n        save()\n    }\n\n    fun captureCreature()',
    1
)

rep('                        Text("VALE DAS FOLHAS", color = Mint, fontWeight = FontWeight.Black, letterSpacing = 2.sp)\n',
    '                        Text(areaName, color = Mint, fontWeight = FontWeight.Black, letterSpacing = 2.sp)\n',
    "region title")
rep('                    TextButton(onClick = { screen = "team" }) {\n',
    '                    if (area < maxArea) TextButton(onClick = { area++; playerX = 4; playerY = 8; message = "Você chegou a $areaName."; save() }) {\n'
    '                        Text("PRÓXIMA ÁREA", color = Gold, fontSize = 10.sp)\n'
    '                    }\n'
    '                    TextButton(onClick = { screen = "team" }) {\n',
    "next region button")
rep('                WorldMap(playerX, playerY, facing, steps) { dx, dy -> movePlayer(dx, dy) }\n',
    '                WorldMap(playerX, playerY, facing, steps, area) { dx, dy -> movePlayer(dx, dy) }\n',
    "region map call")
rep('fun WorldMap(px: Int, py: Int, facing: String, stepCount: Int, onMove: (Int, Int) -> Unit) {',
    'fun WorldMap(px: Int, py: Int, facing: String, stepCount: Int, area: Int, onMove: (Int, Int) -> Unit) {',
    "region map signature")

rep('        val insideLake = nx in 0..2 && ny in 1..3\n        val insideHouse = nx in 5..8 && ny in 0..4\n',
    '        val insideLake = when (area) { 0 -> nx in 0..2 && ny in 1..3; 1 -> nx in 6..8 && ny in 1..3; else -> nx in 2..4 && ny in 0..2 }\n'
    '        val insideHouse = when (area) { 0 -> nx in 5..8 && ny in 0..4; 1 -> nx in 0..2 && ny in 0..4; else -> nx in 6..8 && ny in 0..3 }\n',
    "region collisions")

rep('''            for (y in 0 until rows) for (x in 3..4) {
                drawImage(pathSheet, IntOffset(80, 16), IntSize(16, 16),
                    IntOffset((x * cw).toInt(), (y * ch).toInt()), IntSize(cw.toInt() + 1, ch.toInt() + 1))
            }
''',
'''            if (area == 2) {
                for (y in 4..5) for (x in 0 until cols) {
                    drawImage(pathSheet, IntOffset(80, 16), IntSize(16, 16),
                        IntOffset((x * cw).toInt(), (y * ch).toInt()), IntSize(cw.toInt() + 1, ch.toInt() + 1))
                }
            } else {
                val pathColumns = if (area == 1) 4..5 else 3..4
                for (y in 0 until rows) for (x in pathColumns) {
                    drawImage(pathSheet, IntOffset(80, 16), IntSize(16, 16),
                        IntOffset((x * cw).toInt(), (y * ch).toInt()), IntSize(cw.toInt() + 1, ch.toInt() + 1))
                }
            }
''', "region paths")

rep('''            drawImage(waterSheet, IntOffset(0, 0), IntSize(48, 48), IntOffset(0, (ch * 1.1f).toInt()), IntSize((cw * 2.4f).toInt(), (ch * 2.4f).toInt()))
''',
'''            val lakeX = when (area) { 1 -> (cw * 6f).toInt(); 2 -> (cw * 2f).toInt(); else -> 0 }
            val lakeY = if (area == 2) (ch * 1.2f).toInt() else (ch * 1.1f).toInt()
            drawImage(waterSheet, IntOffset(0, 0), IntSize(48, 48), IntOffset(lakeX, lakeY), IntSize((cw * 2.4f).toInt(), (ch * 2.4f).toInt()))
''', "region lakes")
rep('''            drawImage(houseSheet, IntOffset(32, 112), IntSize(96, 112), IntOffset((cw * 5.25f).toInt(), (ch * .05f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * 4.2f).toInt()))
''',
'''            val houseX = if (area == 1) (cw * .25f).toInt() else (cw * 5.25f).toInt()
            drawImage(houseSheet, IntOffset(32, 112), IntSize(96, 112), IntOffset(houseX, (ch * .05f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * 4.2f).toInt()))
''', "region houses")
rep('''            listOf(0 to 5, 1 to 8, 8 to 5, 8 to 8, 2 to 0).forEach { (tx, ty) ->
''',
'''            val treeSpots = when (area) {
                1 -> listOf(0 to 5, 1 to 8, 8 to 5, 8 to 8, 4 to 0)
                2 -> listOf(0 to 1, 1 to 2, 7 to 1, 8 to 2, 0 to 8, 8 to 8)
                else -> listOf(0 to 5, 1 to 8, 8 to 5, 8 to 8, 2 to 0)
            }
            treeSpots.forEach { (tx, ty) ->
''', "region trees")
rep('''            drawImage(fenceSheet, IntOffset(0, 0), IntSize(32, 16), IntOffset((cw * 5.1f).toInt(), (ch * 3.5f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * .55f).toInt()))
''',
'''            val fenceX = if (area == 1) (cw * .2f).toInt() else (cw * 5.1f).toInt()
            drawImage(fenceSheet, IntOffset(0, 0), IntSize(32, 16), IntOffset(fenceX, (ch * 3.5f).toInt()), IntSize((cw * 3.1f).toInt(), (ch * .55f).toInt()))
''', "region fences")
rep('''        Text("Vila Clover   •   Lago Azul   •   Trilha da Floresta", color = Color(0xFFC5E4D2), fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(top = 5.dp))
''',
'''        Text("$areaName   •   Explore e encontre criaturas", color = Color(0xFFC5E4D2), fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(top = 5.dp))
''', "region footer")

game.write_text(src, encoding="utf-8")
print("Vertical RPG features patched:", game)
