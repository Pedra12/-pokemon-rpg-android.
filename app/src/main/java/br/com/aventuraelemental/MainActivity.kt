package br.com.aventuraelemental

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.min

private val Ink = Color(0xFF172B35)
private val Gold = Color(0xFFFFD477)
private val Leaf = Color(0xFF70B878)
private enum class Page { HOME, WORLD, BATTLE, TEAM }

class MainActivity : ComponentActivity() {
    @Suppress("DEPRECATION")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.decorView.systemUiVisibility = (4 or 1024 or 4096 or 512 or 2)
        window.statusBarColor = android.graphics.Color.TRANSPARENT
        window.navigationBarColor = android.graphics.Color.TRANSPARENT
        setContent { MaterialTheme { ElementalGame() } }
    }
}

@Composable
private fun ElementalGame() {
    var page by remember { mutableStateOf(Page.HOME) }
    var heroX by remember { mutableIntStateOf(4) }
    var heroY by remember { mutableIntStateOf(5) }
    var hp by remember { mutableIntStateOf(24) }
    var wins by remember { mutableIntStateOf(0) }
    var message by remember { mutableStateOf("Bem-vindo a Vale Verde. Uma aventura começa!") }
    var enemyHp by remember { mutableIntStateOf(18) }
    var level by remember { mutableIntStateOf(1) }

    fun move(dx: Int, dy: Int) {
        heroX = (heroX + dx).coerceIn(1, 8)
        heroY = (heroY + dy).coerceIn(1, 8)
        message = listOf("As folhas farfalham ao vento.", "Você ouviu algo entre as árvores.", "O caminho segue para o norte.").random()
    }

    Column(Modifier.fillMaxSize().background(Color(0xFF142B37))) {
        when (page) {
            Page.HOME -> {
                Spacer(Modifier.weight(1f))
                Text("AVENTURA", color = Color.White, fontSize = 34.sp, fontWeight = FontWeight.Black, modifier = Modifier.align(Alignment.CenterHorizontally))
                Text("ELEMENTAL", color = Gold, fontSize = 38.sp, fontWeight = FontWeight.Black, modifier = Modifier.align(Alignment.CenterHorizontally))
                Spacer(Modifier.height(12.dp))
                Text("Uma jornada por um mundo vivo", color = Color(0xFFD5E7D9), modifier = Modifier.align(Alignment.CenterHorizontally))
                Spacer(Modifier.height(34.dp))
                Button(onClick = { page = Page.WORLD }, modifier = Modifier.fillMaxWidth().padding(horizontal = 34.dp), colors = ButtonDefaults.buttonColors(containerColor = Leaf)) { Text("NOVA AVENTURA", color = Ink, fontWeight = FontWeight.Bold) }
                OutlinedButton(onClick = { page = Page.TEAM }, modifier = Modifier.fillMaxWidth().padding(horizontal = 34.dp)) { Text("EQUIPE") }
                Spacer(Modifier.weight(1f))
                Text("PROJETO RECONSTRUÍDO DO ZERO", color = Color(0xFF9BB6B5), fontSize = 10.sp, modifier = Modifier.align(Alignment.CenterHorizontally).padding(bottom = 22.dp))
            }
            Page.WORLD -> {
                Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("VALE VERDE", color = Gold, fontWeight = FontWeight.Black, fontSize = 18.sp)
                    Text("Nv. $level   ♥ $hp/24", color = Color.White, fontWeight = FontWeight.Bold)
                }
                Box(Modifier.weight(1f).fillMaxWidth().padding(horizontal = 10.dp)) {
                    Canvas(Modifier.fillMaxSize()) {
                        val cell = min(size.width / 10f, size.height / 10f)
                        val ox = (size.width - cell * 10) / 2
                        val oy = (size.height - cell * 10) / 2
                        for (y in 0..9) for (x in 0..9) {
                            val grass = if ((x + y) % 3 == 0) Color(0xFF79B96D) else Color(0xFF86C779)
                            drawRect(grass, Offset(ox + x * cell, oy + y * cell), Size(cell + 1, cell + 1))
                            if ((x * 7 + y * 3) % 11 == 0) drawCircle(Color(0xFFB5D98A), cell * .035f, Offset(ox + (x+.5f)*cell, oy + (y+.5f)*cell))
                        }
                        // caminho de pedras
                        for (y in 2..8) drawRect(Color(0xFFD7BD88), Offset(ox + 4*cell, oy + y*cell), Size(cell, cell))
                        for (x in 2..7) drawRect(Color(0xFFD7BD88), Offset(ox + x*cell, oy + 7*cell), Size(cell, cell))
                        // lago
                        drawOval(Color(0xFF4FADD0), Offset(ox + 6.4f*cell, oy + .7f*cell), Size(2.5f*cell, 1.8f*cell))
                        // casas
                        house(ox+cell*.6f, oy+cell*1.1f, cell)
                        house(ox+cell*7.2f, oy+cell*5.2f, cell)
                        // árvores
                        val trees = listOf(1 to 4, 2 to 2, 8 to 2, 8 to 8, 1 to 8, 6 to 4, 3 to 5)
                        trees.forEach { (x,y) ->
                            drawCircle(Color(0xFF326B43), cell*.34f, Offset(ox+(x+.5f)*cell, oy+(y+.42f)*cell))
                            drawCircle(Color(0xFF4C9856), cell*.27f, Offset(ox+(x+.43f)*cell, oy+(y+.34f)*cell))
                            drawRect(Color(0xFF805A3B), Offset(ox+(x+.43f)*cell, oy+(y+.58f)*cell), Size(cell*.14f, cell*.27f))
                        }
                        // NPC
                        drawCircle(Color(0xFFFFD5A4), cell*.19f, Offset(ox+5.5f*cell, oy+4.5f*cell))
                        drawRect(Color(0xFF9A5BC0), Offset(ox+5.31f*cell, oy+4.67f*cell), Size(cell*.38f, cell*.3f))
                        // herói
                        val hx = ox+(heroX+.5f)*cell; val hy = oy+(heroY+.5f)*cell
                        drawCircle(Color(0xFFFFD3A0), cell*.2f, Offset(hx, hy-cell*.16f))
                        drawRect(Color(0xFF315C9B), Offset(hx-cell*.21f, hy-cell*.02f), Size(cell*.42f, cell*.38f))
                        drawRect(Color(0xFF463B35), Offset(hx-cell*.18f, hy+cell*.34f), Size(cell*.14f, cell*.17f))
                        drawRect(Color(0xFF463B35), Offset(hx+cell*.04f, hy+cell*.34f), Size(cell*.14f, cell*.17f))
                    }
                }
                Text(message, color = Color.White, fontSize = 13.sp, modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp))
                Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Control("▲") { move(0,-1) }
                        Row { Control("◀") { move(-1,0) }; Spacer(Modifier.width(8.dp)); Control("▼") { move(0,1) }; Spacer(Modifier.width(8.dp)); Control("▶") { move(1,0) } }
                    }
                    Column(horizontalAlignment = Alignment.End) {
                        Button(onClick = { page = Page.BATTLE; enemyHp = 18; message = "Um espírito selvagem apareceu!" }, colors = ButtonDefaults.buttonColors(containerColor = Gold)) { Text("EXPLORAR", color = Ink) }
                        TextButton(onClick = { page = Page.TEAM }) { Text("EQUIPE", color = Color.White) }
                    }
                }
                Spacer(Modifier.height(10.dp))
            }
            Page.BATTLE -> {
                Text("ENCONTRO SELVAGEM", color = Gold, fontWeight = FontWeight.Black, modifier = Modifier.padding(18.dp))
                Spacer(Modifier.weight(1f))
                Canvas(Modifier.fillMaxWidth().height(250.dp)) {
                    drawRect(Color(0xFF86B96D), Offset(0f,size.height*.56f), Size(size.width,size.height*.44f))
                    drawOval(Color(0xFF3E8C70), Offset(size.width*.48f,size.height*.12f), Size(size.width*.34f,size.height*.34f))
                    drawCircle(Color(0xFFB9E6A1), size.minDimension*.09f, Offset(size.width*.65f,size.height*.28f))
                    drawCircle(Color(0xFF243C43), size.minDimension*.018f, Offset(size.width*.62f,size.height*.26f))
                    drawCircle(Color(0xFF243C43), size.minDimension*.018f, Offset(size.width*.70f,size.height*.26f))
                    drawOval(Color(0xFF315C9B), Offset(size.width*.12f,size.height*.55f), Size(size.width*.28f,size.height*.22f))
                }
                Text("ESPÍRITO DA FLORESTA   ♥ $enemyHp/18", color = Color.White, modifier = Modifier.padding(16.dp))
                Spacer(Modifier.weight(1f))
                Text(message, color = Color.White, modifier = Modifier.padding(16.dp))
                Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { enemyHp -= 6; if (enemyHp <= 0) { wins++; level++; message = "Vitória! Você ganhou experiência."; page = Page.WORLD } else { hp = (hp-3).coerceAtLeast(1); message = "Seu golpe acertou! O inimigo reagiu." } }, modifier = Modifier.weight(1f)) { Text("GOLPE") }
                    Button(onClick = { hp = (hp+8).coerceAtMost(24); message = "Você usou uma poção." }, modifier = Modifier.weight(1f)) { Text("POÇÃO") }
                    OutlinedButton(onClick = { page = Page.WORLD }, modifier = Modifier.weight(1f)) { Text("FUGIR") }
                }
            }
            Page.TEAM -> {
                Text("SUA EQUIPE", color = Gold, fontWeight = FontWeight.Black, fontSize = 24.sp, modifier = Modifier.padding(22.dp))
                Spacer(Modifier.height(25.dp))
                Text("BRASA", color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.CenterHorizontally))
                Text("Criatura elemental • Nv. $level", color = Color(0xFFD5E7D9), modifier = Modifier.align(Alignment.CenterHorizontally))
                Spacer(Modifier.weight(1f))
                Button(onClick = { page = Page.WORLD }, modifier = Modifier.fillMaxWidth().padding(18.dp)) { Text("VOLTAR AO MUNDO") }
            }
        }
    }
}

@Composable
private fun Control(label: String, action: () -> Unit) {
    FilledTonalButton(onClick = action, modifier = Modifier.size(48.dp), contentPadding = PaddingValues(0.dp)) { Text(label, fontSize = 20.sp) }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.house(x: Float, y: Float, cell: Float) {
    drawRect(Color(0xFFB96D4A), Offset(x, y+cell*.35f), Size(cell*1.35f, cell*.9f))
    val roof = PathBuilder()
    drawRect(Color(0xFF75413D), Offset(x-cell*.12f, y+cell*.15f), Size(cell*1.58f, cell*.28f))
    drawRect(Color(0xFF5A382F), Offset(x+cell*.5f, y+cell*.68f), Size(cell*.28f, cell*.57f))
}
private class PathBuilder
