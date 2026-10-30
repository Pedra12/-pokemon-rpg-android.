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
    '                        Text("EQUIPE (\${1 + capturedCreatures.split("|").count { it.isNotBlank() }})", color = Gold)\n'
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
    '                    StatCard("CRIATURAS", "\${1 + capturedCreatures.split("|").count { it.isNotBlank() }}", Modifier.weight(1f))\n',
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
                        Text("\${index + 1}. $name", color = Paper, modifier = Modifier.fillMaxWidth().padding(vertical = 5.dp))
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

game.write_text(src, encoding="utf-8")
print("Vertical RPG features patched:", game)
