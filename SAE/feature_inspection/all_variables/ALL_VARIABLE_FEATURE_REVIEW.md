# All-Variable SAE Feature Review

Five mean-pooled SAE candidates were selected for each of the 40 linguistic variables before test evidence was consulted.

The purpose of this document is exploratory feature interpretation for later causal work. A candidate is **not automatically rejected** because of a test-direction mismatch, imperfect specificity, subgroup weakness, or a lower prior SAE evidence tier. Those properties should be treated as evidence weights rather than binary barriers.

# Variable 01: Subject expression / pro-drop

- Original SAE evidence tier: **D**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 8431

- selection: `original_trainval_selected`
- train effect: `+0.869`
- validation effect: `+0.101`
- test effect: `-0.248`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.149`

### Top natural activations

1. `act=1.1710` `token='▁sergi'`  
   Galerist atölyesinde sergi planları üzerinde tartışırken eski bir yardımcı ressamın fikri yeniden canlanmaya başladı.

2. `act=1.1427` `token='▁iş'`  
   İşyerinde iş güvenliği zorunlulukları çalışanların sağlığını korumak için titizlikle uygulanıyor.

3. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmen, öğrencilerin anlayabileceği basit dille konuları anlattı.

4. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmen, dün yapılan sınavda en yüksek puanı alan öğrenciye bir övgü verdi.

5. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmenimizin dediğine göre bu yılki sınıfta öğrencilerin çoğu hem derslere gelmemek hem de ödevlerini yapmamak konusunda oldukça isteksizmiş.

6. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmen, öğrencilerine "söylediğimiz"i unutmadan çalıştırmalarını istedi.

7. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmen anlattı.

8. `act=1.1351` `token='▁öğretmen'`  
   Okulda öğretmen öğrencilere ders anlattı.

## Candidate 2: feature 8041

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.863`
- validation effect: `+0.962`
- test effect: `+0.970`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.921`

### Top natural activations

1. `act=0.8645` `token='▁الاحت'`  
   الاحتجاجات مستمرة في الضغط على الحكومة للرد بسرعة.

2. `act=0.8143` `token='▁خلف'`  
   خلف الجبل الأسود الذي يبرز على الأفق، تتدلى الغيوم الكثيفة مهددة بالعاصفة التي سبق أن نذرت السكان ببرد قارس هبط فجأةً من سماء كان يتوهّج قبل لحظات بلون الذهب المذاب.

3. `act=0.8138` `token='▁我們'`  
   我們明天早上七點出發。

4. `act=0.8138` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

5. `act=0.8138` `token='▁我們'`  
   我們馬上啟程去機場。

6. `act=0.8004` `token='▁مر'`  
   مرحباً بالزائر الجديد.

7. `act=0.8004` `token='▁مر'`  
   مرحباً، ماذا تحب أن تأكل اليوم؟

8. `act=0.8004` `token='▁مر'`  
   مرحباً يا فريق، إليك التقرير الشهري الجديد.

## Candidate 3: feature 15659

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.851`
- validation effect: `+0.947`
- test effect: `+0.949`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `4`
- specificity ratio: `0.920`

### Top natural activations

1. `act=1.3679` `token='.'`  
   Каждый студент в группе активно участвовал в обсуждении темы, приводил собственные примеры и пытался показать, как то или иное положение может применяться в реальной жизни.

2. `act=1.3672` `token='.'`  
   It is clear from the assessment reports and classroom observations that the students have fully grasped the core concepts of algebra and are now ready to move on to more advanced mathematical topics.

3. `act=1.3639` `token='.'`  
   Each student who completed the summer research program presented their findings at the conference, and each presentation was distinct, revealing how every participant had approached the project with their own method and curiosity.

4. `act=1.3621` `token='.'`  
   In the seminar room filled with eager students, she spoke eloquently about the power of narrative in art, using he and they throughout her talk to create a sense of collective reflection and personal engagement.

5. `act=1.3601` `token='.'`  
   After the teacher explained the concept clearly, the students began to understand the material much better.

6. `act=1.3563` `token='.'`  
   Consequently, after the students completed the extensive research project on sustainable agricultural practices, their understanding of ecological systems significantly deepened, which directly influenced the quality of their final presentations and subsequent class discussions.

7. `act=1.3533` `token='.'`  
   She was able to grasp the complex theories quickly, which enabled her to help others understand difficult concepts during group study sessions.

8. `act=1.3498` `token='.'`  
   The students spent the entire afternoon working on their group projects, making steady progress toward completing each assigned task.

## Candidate 4: feature 10169

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.856`
- validation effect: `+0.963`
- test effect: `+0.967`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `4`
- specificity ratio: `0.904`

### Top natural activations

1. `act=2.1726` `token='▁Ру'`  
   Руководитель департамента отказался комментировать слухи о предстоящих сокращениях, подчеркнув, что никаких решений ещё не принято и что все ресурсы всё ещё будут использоваться в полном объёме.

2. `act=2.1726` `token='▁Ру'`  
   Руководитель отметил, что живые примеры в учебнике лучше привлекают внимание студентов, чем абстрактные формулы.

3. `act=2.1726` `token='▁Ру'`  
   Руководствуясь мнением экспертов, вице-президент отдал указание пересмотреть бюджет на следующий квартал.

4. `act=2.1726` `token='▁Ру'`  
   Руководитель оценил проект и команду.

5. `act=2.1726` `token='▁Ру'`  
   Руководителю театра всегда нужен поддерживающий глаз критика.

6. `act=2.1726` `token='▁Ру'`  
   Руководитель отдал оборудование команде для тренировок.

7. `act=2.1726` `token='▁Ру'`  
   Руководитель оценил работу сотрудника перед совещанием.

8. `act=2.1726` `token='▁Ру'`  
   Руководитель отдела назначил трём сотрудникам дополнительные задачи и проследил за их выполнением.

## Candidate 5: feature 1175

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.855`
- validation effect: `+0.959`
- test effect: `+0.968`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `4`
- specificity ratio: `0.895`

### Top natural activations

1. `act=1.3740` `token='▁Paint'`  
   Paintings hang quietly on the museum walls.

2. `act=1.3740` `token='▁Paint'`  
   Paintings transform empty walls into windows of imagination.

3. `act=1.3740` `token='▁Paint'`  
   Paintings in that style rarely sell well in this town.

4. `act=1.3740` `token='▁Paint'`  
   Painters often gather at the old square to capture the morning light.

5. `act=1.3740` `token='▁Paint'`  
   Painters often work late into the night.

6. `act=1.3740` `token='▁Paint'`  
   Painters often get inspired by nature.

7. `act=1.3740` `token='▁Paint'`  
   Painters were setting up their easels along the riverside walkway just as the morning light began to change.

8. `act=1.3740` `token='▁Paint'`  
   Paintings line the walls in that gallery.

---

# Variable 02: basic_constituent_order

- Original SAE evidence tier: **C**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.622**

## Candidate 1: feature 9791

- selection: `original_trainval_selected`
- train effect: `+0.823`
- validation effect: `+0.807`
- test effect: `+0.033`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.753`

### Top natural activations

1. `act=1.1105` `token='ము'`  
   మా బృందం ఈ ప్రాజెక్టును మేము కలిసి పూర్తి చేయడానికి ప్రయత్నిస్తోంది.

2. `act=1.0197` `token='▁सब'`  
   शिक्षा में उनकी रुचि हम सब पर गर्व कराती है।

3. `act=0.9606` `token='▁सभी'`  
   मेरी बहन के मिलाप में बनाई गई वो खास डिश के स्वाद हम सभी ने पसंद किया, जो अपन आम रसोई के तुलना में बेहतरीन पकवान के रूप में सामने आई थी।

4. `act=0.9589` `token='▁सब'`  
   क्रिकेट में उसकी पारी हम सब को प्रेरित करती है।

5. `act=0.9412` `token='ము'`  
   మా కుటుంబంలో అందరూ కలిసి ఉన్నప్పటికీ, ఈ నిర్ణయం మాత్రం మేము ఇద్దరు తీసుకున్నాము.

6. `act=0.9173` `token='▁پر'`  
   کھیل کے نتیجے میں کوچ کا فیصلہ سب پر واضح ہو گیا۔

7. `act=0.9055` `token='画'`  
   木版画は、制作方法が絵画と対照的だ。

8. `act=0.8989` `token='மும்'`  
   வேற்று மக்கள் அனுபவிக்கும் சுற்றுச்சூழலை நாமும் பாதுகாக்க வேண்டும்.

## Candidate 2: feature 932

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.695`
- validation effect: `+0.750`
- test effect: `+0.426`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.751`

### Top natural activations

1. `act=1.7930` `token='▁a'`  
   Les matches de rugby qu’elle a joués étaient plus intenses que ceux auxquels j’ai assistés.

2. `act=1.6796` `token='il'`  
   Il avait réservé son billet en avance pour le long voyage en train à travers les montagnes, mais en arrivant à la gare, il découvrit que le siège qu’il avait choisi était déjà occupé par une autre passagère.

3. `act=1.6473` `token='ils'`  
   Il semble probable que les parents du jeune homme, après des années d’absence mystérieuse, soient enfin revenus dans la région pour réparer les liens familiaux qu’ils avaient laissés en friche.

4. `act=1.6389` `token='elle'`  
   Il admire la forêt qu'elle traverse, subjugué par la beauté qu'il découvre à chaque pas.

5. `act=1.6231` `token='▁olivat'`  
   He puhuivat pitkään kahvissa etsien yhteisiä harrastuksia ja vertaillen viimeisiä elokuvia, joita he olivat katsoneet.

6. `act=1.5976` `token='▁avait'`  
   Il ne restait plus que le couvercle de la marmite qu’elle avait posée sur la gazinière avant d’aller chercher les épices dans l’armoire au-dessus du lave-vaisselle.

7. `act=1.5923` `token='▁она'`  
   Её новый компьютер, который она купила вчера, уже сломался, и соседка, у которой осталась её старая мышка от предыдущего ноутбука, сказала, что починить его будет слишком дорого.

8. `act=1.5869` `token='▁on'`  
   Talon takana kasvaa useita erilaisia puita ja pensaita, joita kaunis talvi on peittänyt tiiviisti lumen alla.

## Candidate 3: feature 7834

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.679`
- validation effect: `+0.666`
- test effect: `-0.155`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.509`

### Top natural activations

1. `act=0.9866` `token='ंगल'`  
   सूरज की किरणें जंगल में प्रकाश के झरने के रूप में झुकीं थीं, जहाँ चिड़ियाँ गाती रहीं और पत्तियाँ हल्की हवा में हिलती रहीं।

2. `act=0.9866` `token='ंगल'`  
   सूरज की किरणें जंगल में झूलते हुए धीरे-धीरे पत्तियों के बीच खेलती रहीं और घास को जीवित भरे हरे रंग में डूबा दिया।

3. `act=0.9683` `token='▁herkes'`  
   Birçok turist, Türkiye'deki doğal hava koşullarına karşı ne kadar dayanıklıysa olsa da, bu şehirdeki sokak kavurma dumanı ve havanın içine giren sıcak kebap kokuları herkesi oldukça etkiledi ve "burada taze hava almak" ifadesinin ne anlama geldiğini anlamlı bir şekilde tekrar düşünmeye zorladı.

4. `act=0.9231` `token='▁herkes'`  
   Bir parkta çocuklar top oynarken yaşlı bir adam yürüyüş yaparken onları seyrediyor ve bir süre sonra gençlerin hızına yetişemeyip nefes nefese kalmaları herkesi güldürüyor.

5. `act=0.9066` `token='▁herkes'`  
   Köşkten sofraya uzanan masalarda lezzetli yemeklerin kokusu herkesi kendine çekerdi.

6. `act=0.9031` `token='▁herkes'`  
   Atatürk Havaalanı'ndan Kahire'ye giden ve yoğun yolcu alana sahip olan ilk uçuşta, sabah erken kalkış yapmak zorunda olan bu ekibin profesyonel duruşu herkesi etkilemişti.

7. `act=0.9008` `token='▁mahalle'`  
   Fırıncıdan taze çıkan ekmeklerin kokusu mahalleye hemen yayıldı.

8. `act=0.8936` `token='▁herkes'`  
   Toplantıda alınan kararlar herkes için geçerli.

## Candidate 4: feature 13096

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.677`
- validation effect: `+0.633`
- test effect: `-0.019`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.499`

### Top natural activations

1. `act=1.0481` `token='▁द्वारा'`  
   कार्यालय में उपस्थिति की जाँच आमतौर पर प्रबंधक द्वारा की जाती है।

2. `act=1.0389` `token='▁द्वारा'`  
   हमने अपने बच्चों को उनकी माँ द्वारा प्रेरित करके पब्लिक ट्रांसपोर्ट के नियमों के बारे में सीखने के लिए उत्साहित कर दिया।

3. `act=1.0358` `token='▁द्वारा'`  
   मेरे पिता ने जो खाना बनाया हुआ था उसके साथ बच्चों की माँ द्वारा लाए गए नाशपाती का जूस ले लिया और हम सभी में खेल के बाद लगी हुई ऊब फट गई।

4. `act=1.0338` `token='▁द्वारा'`  
   कर्मचारी को नए मिठाई के स्वाद का आनंद लेने के लिए प्रबंधन द्वारा एक छोटा सा तोहफा मिला।

5. `act=1.0207` `token='▁द्वारा'`  
   मेरी पुस्तकें मेरे शिक्षक द्वारा संपादित की गईं।

6. `act=1.0136` `token='▁द्वारा'`  
   उसकी नई कार पुलिस द्वारा बरामद कर ली गई।

7. `act=1.0134` `token='▁द्वारा'`  
   विद्यार्थी को अपने प्रबंधक द्वारा कलेजा छोड़े जाने के लिए प्रेरित किया गया।

8. `act=1.0107` `token='▁द्वारा'`  
   विद्यार्थी को शिक्षक द्वारा पढ़ाए गए अध्याय में बहुत से नए शब्द मिले।

## Candidate 5: feature 9064

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.768`
- validation effect: `+0.774`
- test effect: `+0.244`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.365`

### Top natural activations

1. `act=1.1032` `token='lerin'`  
   Karasal ve okyanuslarda kaydedilen ısınma eğilimi, iklim bilimcilerin büyük bir çoğunluğunun öne sürdükleri üzere, doğal çevresel dengeleri ciddi şekilde etkileyebiliyor.

2. `act=1.0552` `token='nın'`  
   Kocaman duvarlar boyunca sergilenen resimler, sanatçının geçmiş atölyelerindeki çalışmalardan derlenmişti.

3. `act=1.0146` `token='nin'`  
   Bilimsel bir sinema festivalinde, özellikle süper iletken maddelerle ilgili filmlerde karakterlerin ne kadar net ifade edilemeyeceğini ve onların yerine geçen sesli açıklamaların teknik detayları nasıl daha etkili aktarabildiğini düşünmek her ziyaretçinin kendi yorum yeteneğine yönelik yeni bir farkındalık kazanmasına neden oluyor.

4. `act=0.9997` `token='▁tarafından'`  
   Resimdeki karakterlerin rolleri sanatçı tarafından farklı boyutlarda işlenirken, dinleyiciyi ikinci planda bırakarak olayların gerçekliğini ön plana çıkarıyor.

5. `act=0.9911` `token='▁tarafından'`  
   Gökyüzünde hareket eden, zaman zaman bulutlara gizlenen ve her gecede belirli bir düzen içinde doğu ve batı arasında seyahat eden Ay'ın hareketleri, astronomlar tarafından özellikle küresel ısınma etkilerinin gökyüzüne yansıtıldığı son yıllarda daha dikkatle incelenmeye başlanmıştır.

6. `act=0.9844` `token='ın'`  
   Görünüşe göre bu tür veriler, yazarın başka bir kaynaktan derlediği şeylere dayanıyor.

7. `act=0.9671` `token='ın'`  
   Onun çalınmış fikirlerinin yer aldığı eserler, yazarın uzun zamandır takip ettiği yaratıcılık tarzıydı.

8. `act=0.9437` `token='nın'`  
   Gösteri boyunca dinleyicilere hissettirilen sessizlik, sanatçının çarpıcı tiyatro efekti yaratmak istediği ruhu yansıtmıştı.

---

# Variable 03: nominal_modifier_order

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.456**

## Candidate 1: feature 4426

- selection: `original_trainval_selected`
- train effect: `-0.566`
- validation effect: `-0.076`
- test effect: `+0.199`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.671`

### Top natural activations

1. `act=1.6063` `token='▁su'`  
   El gerente revisó los informes del primer trimestre, señaló que las proyecciones iniciales eran optimistas y asignó a su equipo la tarea de ajustar los planes estratégicos para alinearlos con los resultados reales obtenidos en el último mes.

2. `act=1.6038` `token='▁su'`  
   El tío de mi prima, que acaba de regresar del extranjero donde trabajaba, nos contó una historia conmovedora sobre cómo ayudó a su sobrino menor a superar el miedo a hablar en público.

3. `act=1.5995` `token='▁su'`  
   Aunque el profesor insistió en que todos leyeran el capítulo entero antes de la clase, María solo se tomó unos minutos para repasar las partes que le parecieron más importantes y después ayudó a su hermano menor con la tarea de matemáticas.

4. `act=1.5796` `token='▁su'`  
   Todos los sábados por la tarde, Marta ayudaba a su madre a preparar la cena para toda la familia.

5. `act=1.5420` `token='▁su'`  
   La niña estaba ayudando a su abuela en la cocina.

6. `act=1.5374` `token='▁su'`  
   María le pidió a su hermano que trajera agua y le dijo a Pedro que encendiera las luces.

7. `act=1.5356` `token='▁su'`  
   A pesar de que le había prometido a su primo que cuidaría sus manos mientras trabajaban en el vivero, al final terminó cortándose accidentalmente un dedo al separar unas plantas jóvenes y tuvo que pedirle ayuda a otro vecino para curárselo antes de que el muchacho se diera cuenta.

8. `act=1.5315` `token='▁su'`  
   La hermana mayor del niño ayudó a su sobrino pequeño a preparar el desayuno.

## Candidate 2: feature 10647

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.570`
- validation effect: `-0.197`
- test effect: `-0.141`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.297`

### Top natural activations

1. `act=0.8424` `token="'"`  
   From my vantage point near the stove, I can see that the sauce is simmering just beyond arm's reach on the back burner.

2. `act=0.8203` `token="'"`  
   I often find myself reviewing the same concepts with students who just don't seem to retain them.

3. `act=0.8114` `token="'"`  
   I already made dinner last night, so we don't need to cook again today.

4. `act=0.8060` `token="'"`  
   I realized that students understand the material better when I say "that" in explanations, even if they don't need it.

5. `act=0.7995` `token='’'`  
   It was the roasted garlic that made the difference, really — I mean, even though we both followed the same recipe, that was what made mine taste so much better, don’t you think?

6. `act=0.7994` `token="'"`  
   I've already made dinner, so we don't need to worry about that.

7. `act=0.7982` `token="'"`  
   If someone asks if they can borrow your TV, you probably don't want them watching it all week.

8. `act=0.7935` `token="'"`  
   If you had asked me earlier, I might have said yes, but now that we've already talked it over and I know how much work it involves, I really don't think I can commit to helping out right now.

## Candidate 3: feature 11666

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.568`
- validation effect: `+0.431`
- test effect: `+0.302`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.250`

### Top natural activations

1. `act=1.2716` `token='▁fue'`  
   Lo que más me impactó del curso fue la claridad con que explica conceptos complejos.

2. `act=1.2311` `token='▁fue'`  
   Lo que más me ayudó en la escuela fue que me escucharan.

3. `act=1.2204` `token='▁fue'`  
   Lo que más me impresionó del viaje fue la antigua estación de tren abandonada en el centro de la ciudad.

4. `act=1.2204` `token='▁fue'`  
   Lo que más me impresionó del viaje fue el amanecer desde la cima del tren.

5. `act=1.2187` `token='▁was'`  
   What stands out to me from the mayor's speech was how little he actually proposed.

6. `act=1.2074` `token='▁fue'`  
   Lo que más me gustó del viaje fue el paisaje que vimos al llegar a la cima del cerro.

7. `act=1.1950` `token='▁es'`  
   Lo que me gusta de este cuadro es el detalle con que pintó las flores.

8. `act=1.1934` `token='▁fue'`  
   Lo que más me sorprendió durante mi primer mes en el nuevo trabajo fue precisamente la manera en que cada persona resolvía los problemas, sin parecerse del todo a cómo yo lo haría.

## Candidate 4: feature 7775

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.569`
- validation effect: `-0.141`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.869`

### Top natural activations

1. `act=1.7741` `token='’'`  
   If we missed the train, we’d be stuck here all night.

2. `act=1.7727` `token='’'`  
   That friend of mine, she’s been nothing but trouble since the start.

3. `act=1.7670` `token='’'`  
   It seems likely that if we start reviewing the material together tonight, he’ll understand the assignment by tomorrow.

4. `act=1.7648` `token='’'`  
   When we arrive at the train station tomorrow, we’ll grab a coffee at that little café near the platform where we can sit by the window and watch the travelers come and go while our train gets cleaned and prepared for its next journey.

5. `act=1.7647` `token='’'`  
   The woman who had invited me to her book club that afternoon was surprised when I arrived early, having forgotten the time while rereading the novel she’d recommended.

6. `act=1.7644` `token='’'`  
   Pack your hiking boots," she said, glancing at the weather forecast on her phone, "because if it holds up, we’ll be scrambling up that trail before sunrise.

7. `act=1.7630` `token='’'`  
   Would you mind turning down the music a bit—I need to check my blood pressure and can’t hear myself think.

8. `act=1.7622` `token='’'`  
   If I hadn’t left the cookies in the oven too long, they’d still be soft and chewy instead of dry and crumbly.

## Candidate 5: feature 8006

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.670`
- validation effect: `+0.256`
- test effect: `+0.174`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.739`

### Top natural activations

1. `act=1.2011` `token='▁beyond'`  
   Students often find that learning is more engaging when it extends beyond the classroom and into real-world experiences like museum visits or cultural exchanges.

2. `act=1.1876` `token='▁into'`  
   The patient's detailed medical history provides valuable insights into her chronic condition.

3. `act=1.1800` `token='▁with'`  
   University students often struggle with time management.

4. `act=1.1775` `token='▁beyond'`  
   A mother's love endures beyond time, shaping generations through quiet strength and unwavering devotion.

5. `act=1.1611` `token='▁and'`  
   Step back and let the colors guide your imagination.

6. `act=1.1611` `token='▁and'`  
   Step back and let the artist finish the mural before taking photos.

7. `act=1.1591` `token='▁into'`  
   The tree’s roots extend deep into the rocky soil.

8. `act=1.1580` `token='▁with'`  
   According to a recent study published in the *Journal of Educational Psychology*, many students reported that they found collaborative learning more effective when structured guidance was provided by instructors familiar with group dynamics.

---

# Variable 04: case_marking

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 13269

- selection: `original_trainval_selected`
- train effect: `+0.511`
- validation effect: `+0.390`
- test effect: `+0.585`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.758`

### Top natural activations

1. `act=0.6652` `token='▁ülke'`  
   Cumhurbaşkanının ülkeye iadesiyle ilgili olarak yasal prosedürler tamamlandı.

2. `act=0.6076` `token='▁parti'`  
   Malgré le soutien indéfectible des partis d'opposition à la réforme fiscale proposée, les députés du gouvernement ont voté en faveur de son adoption, ce qui a suscité des critiques virulentes dans les rangs de leurs électeurs.

3. `act=0.6072` `token='▁நாட்ட'`  
   எங்கள் நிறுவனம் இந்தத் தீர்மானத்துடன் நாட்டின் மற்றப்பகுதி கணிசமாக உறவு கொண்டிருக்கின்றது.

4. `act=0.5973` `token='▁parti'`  
   Kamuoyunun büyük bir kısmı milletvekillerinin partilere sadakatlerini halkın refahına göre değil, siyasi iktidarın çıkarlarına göre değerlendirdiğini düşündüğü için bu tür kararların onlarca bin seçmenin oylarını etkileyebileceğinden emin.

5. `act=0.5911` `token='▁ülke'`  
   İş için ülkeyi dolaşırken bir otobüsle saatlerce yol almam gerekti.

6. `act=0.5835` `token='▁parti'`  
   Komşularımızın partisine kırmızı elbise giyerek gittik.

7. `act=0.5776` `token='▁parti'`  
   Cumhurbaşkanının partisinden bir sözcü, ekonominin bu yılki performansına değindi.

8. `act=0.5679` `token='▁parti'`  
   Olsa olsa, bu kararın kamuya faydası dokunmazken parti içi oyda kazanmak amaçlanıyordu.

## Candidate 2: feature 9071

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.586`
- validation effect: `+0.727`
- test effect: `+0.657`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.727`

### Top natural activations

1. `act=1.2479` `token='▁нет'`  
   На столе нет пищи.

2. `act=1.2214` `token='▁нет'`  
   У неё сегодня нет симптомов простуды, и она чувствует себя отлично.

3. `act=1.2123` `token='▁нет'`  
   На кухне нет моей сковородки.

4. `act=1.2051` `token='▁есть'`  
   У брата есть старинная гитара.

5. `act=1.2051` `token='▁есть'`  
   У брата есть новый альбом с традиционной музыкой.

6. `act=1.2051` `token='▁есть'`  
   У брата есть своя машина.

7. `act=1.2051` `token='▁есть'`  
   У брата есть своя машина, а у меня — нет.

8. `act=1.2051` `token='▁есть'`  
   У брата есть старший сын.

## Candidate 3: feature 9920

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.480`
- validation effect: `-0.431`
- test effect: `-0.348`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.700`

### Top natural activations

1. `act=0.7857` `token='▁tableau'`  
   Si ce tableau avait été exposé au Musée d'Orsay lors de l'exposition rétrospective, les critiques auraient peut-être changé leur avis sur l'influence de l'impressionnisme dans ses œuvres, mais comme il a été refusé par le comité, il n'a jamais fait partie de la conversation artistique dominante.

2. `act=0.7857` `token='▁tableau'`  
   Si ce tableau avait été peint plus tôt, le musée l'aurait exposé cette année.

3. `act=0.7857` `token='▁tableau'`  
   Si ce tableau m'était apparu plus tôt, j'aurais changé mon avis.

4. `act=0.7732` `token='▁tableau'`  
   Je me suis toujours senti le cœur attaché à ces tableaux qu’on retrouve dans les musées de mon enfance.

5. `act=0.7486` `token='▁tableau'`  
   Le peintre féminin expose des tableaux qui illustrent ses visions créatives et lumineuses.

6. `act=0.7433` `token='▁tableau'`  
   Ces tableaux de famille racontent des histoires uniques.

7. `act=0.7433` `token='▁tableau'`  
   Ces tableaux, qu’on admire dans le petit salon, me rappellent les vacances en Provence.

8. `act=0.7433` `token='▁tableau'`  
   Ces tableaux de ma grand-mère, si détaillés, reflètent une époque où l'art local était encore vivant dans chaque village.

## Candidate 4: feature 3534

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.540`
- validation effect: `+0.663`
- test effect: `+0.718`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.215`

### Top natural activations

1. `act=2.2984` `token='lor'`  
   Weil er unpünktlich war, verlor er den Job.

2. `act=2.2923` `token='rt'`  
   Normalerweise kümmert sich die Mutter um die täglichen Haushaltsarbeiten, während der Vater meistens für die finanzielle Sicherheit des Haushalts sorgt und sich außerdem häufig um die Organisation außerhalb des Privathaushalts, wie zum Beispiel Freizeitaktivitäten oder soziale Termine, bemüht.

3. `act=2.2910` `token='te'`  
   Nachdem sie lange über den Streit gesprochen hatten, bot er ihr seine Hand zum Frieden an, und obwohl sie zögernd nickte, spürte man, dass die alte Freundschaft langsam wiederkehren wollte.

4. `act=2.2762` `token='chten'`  
   Auch wenn die Regierung verspricht, die Strompreise zu senken, befürchten viele Haushalte weiterhin, dass die Kosten im nächsten Jahr erneut steigen werden.

5. `act=2.2664` `token='lor'`  
   Trotz der intensiven Trainingseinheiten verlor der Athlet das Wettrennen knapp.

6. `act=2.2555` `token='▁plant'`  
   Weil die Ergebnisse der letzten Untersuchung unklar blieben, plant das Team eine neue Studie durchzuführen, um die Hypothese genauer zu testen.

7. `act=2.2548` `token='e'`  
   Nachdem der Patient die Therapie abgeschlossen hatte, verbesserte sich sein Gesundheitszustand deutlich.

8. `act=2.2519` `token='e'`  
   Nachdem der Spieler intensiv trainiert hatte, verbesserte sich seine Leistung deutlich im nächsten Wettkampf.

## Candidate 5: feature 11875

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.567`
- validation effect: `+0.436`
- test effect: `+0.663`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.175`

### Top natural activations

1. `act=0.7895` `token='▁fosse'`  
   Em nenhum desses projetos culturais foi necessário mencionar o sujeito da ação para que os objetivos fossem claros, já que o contexto institucional e a autoridade envolvida deixavam implícita a responsabilidade.

2. `act=0.7860` `token='▁puisse'`  
   Il est indispensable que les étudiants comprennent bien les fondamentaux de chaque discipline avant de s'engager dans des projets plus complexes, afin qu'ils puissent construire solidement leurs connaissances et développer un esprit critique mû par la rigueur et l'autonomie.

3. `act=0.7802` `token='▁puisse'`  
   Il faut absolument que les enfants terminent leurs devoirs avant le dîner, afin qu’ils puissent se reposer tranquillement et que tout le monde soit prêt pour le spectacle de fin d’année auquel nous avons tous promis d’assister.

4. `act=0.7659` `token='▁aprende'`  
   En la exposición de arte digital, se proyectaron imágenes que reflejaban cómo los algoritmos aprenden a identificar patrones en grandes volúmenes de datos.

5. `act=0.7646` `token='▁aprende'`  
   Cada mañana, observo cómo los algoritmos aprenden de los datos que les proporcionamos.

6. `act=0.7613` `token='▁puisse'`  
   On doit veiller à ce qu'elles puissent s'adapter aux changements climatiques.

7. `act=0.7533` `token='▁aprende'`  
   Es raro que los profesores noten cuánto los alumnos aprenden por observación en lugar de explicación directa.

8. `act=0.7323` `token='▁pudiera'`  
   El profesor le pidió al estudiante que repitiera la respuesta en voz alta para que todos pudieran escucharla.

---

# Variable 05: morphosyntactic_alignment

- Original SAE evidence tier: **B1**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.911**

## Candidate 1: feature 7247

- selection: `original_trainval_selected`
- train effect: `-0.695`
- validation effect: `-0.693`
- test effect: `-0.665`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.771`

### Top natural activations

1. `act=1.6231` `token=','`  
   Lei mi ha telefonato mentre ero fuori, ma non ho risposto.

2. `act=1.6155` `token=','`  
   Вчера мы закончили тренировку рано, так как решили повторить материал уже сегодня вечером.

3. `act=1.6108` `token=','`  
   Я пришёл на работу рано, чтобы успеть подготовить документы к встрече с клиентом.

4. `act=1.6093` `token=','`  
   Вчера я закончила работу рано, потому что всё успела сделать к обеду.

5. `act=1.5922` `token=','`  
   No tomaba medicamentos desde hacía semanas, pero su fiebre persistía igual.

6. `act=1.5901` `token=','`  
   Пироги с капустой я испёк ещё вчера, а сейчас уже все съели.

7. `act=1.5864` `token=','`  
   Сергей още работеше по проекта си отпреди месец, когато босът го повика в кабинета.

8. `act=1.5838` `token=','`  
   Вчера мы закончили проект вовремя, и сегодня начали обсуждать новый заказ с клиентом.

## Candidate 2: feature 9810

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.692`
- validation effect: `-0.674`
- test effect: `-0.667`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.732`

### Top natural activations

1. `act=2.3180` `token='▁درا'`  
   دراستا جالستا في المدرسة مع صديقتي.

2. `act=2.3059` `token='▁تبر'`  
   تبرع المجتمع المحلي بمائة كيس من المواد الغذائية لمساعدة المتضررين.

3. `act=2.2923` `token='▁حل'`  
   حلّى المطبخ رائحة العود.

4. `act=2.2923` `token='▁حل'`  
   حلّ سكانُ القرية الصغيرة في حديقةٍ من النخيل قديمة.

5. `act=2.2923` `token='▁حل'`  
   حلّيت الغاباتُ الجليلتان في شمال البلاد بعد الأمطار.

6. `act=2.2923` `token='▁حل'`  
   حلّت العائلة بالغة الجوع حول الطاولة لتناول الطعام بعد الانتهاء من الزراعة.

7. `act=2.2923` `token='▁حل'`  
   حلت الكفتة مع البطاطس المسلوقة في وعاء خشبي صغير، رائحتها اللذيذة تفوح من جانبي.

8. `act=2.2923` `token='▁حل'`  
   حلوا كُبَّة الكسكس التقليدية، تزدان بصلصة التبولة الطازجة والليمون.

## Candidate 3: feature 14174

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.691`
- validation effect: `-0.680`
- test effect: `-0.655`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.731`

### Top natural activations

1. `act=2.6228` `token='▁我們'`  
   我們馬上啟程去機場。

2. `act=2.6228` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

3. `act=2.6228` `token='▁我們'`  
   我們明天早上七點出發。

4. `act=2.4043` `token='▁해외'`  
   해외여행 시 교통카드를 미리 준비해 두면 도시 내 이동이 훨씬 수월해집니다.

5. `act=2.4005` `token='▁這'`  
   這幅畫的風格很接近當代。

6. `act=2.4005` `token='▁這'`  
   這趟旅程中，他們走過這條路，遠遠望著那座山。

7. `act=2.4005` `token='▁這'`  
   這碗湯要端到廚房去。

8. `act=2.4005` `token='▁這'`  
   這位醫生剛離開診所，我現在還坐在這裡，手裡拿著他剛給我的藥物說明，心裡擔心這種遠處的治療方式是否對我在這個階段的病情真的有效。

## Candidate 4: feature 1199

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.691`
- validation effect: `-0.684`
- test effect: `-0.648`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.730`

### Top natural activations

1. `act=3.9123` `token='▁我們'`  
   我們明天早上七點出發。

2. `act=3.9123` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

3. `act=3.9123` `token='▁我們'`  
   我們馬上啟程去機場。

4. `act=3.8989` `token='▁چک'`  
   چکن میں سے پانی نکلنے لگا تو درختوں کے سائے میں جا بیٹھے۔

5. `act=3.8989` `token='▁چک'`  
   چکر لگانے والوں نے دریا کے کنارے ہی پانی پیا۔

6. `act=3.8975` `token='▁النب'`  
   النباتات المذكرة المنخفضة تتماشى مع الزراعة المستدامة في هذه المنطقة الصحراوية.

7. `act=3.8796` `token='▁Golf'`  
   Golfers often overlook the value of regular practice on short putts.

8. `act=3.8775` `token='▁کچھ'`  
   کچھ خاندانوں نے اپنی کھجور کا تیل مفت تقسیم کرنے کا فیصلہ کیا۔

## Candidate 5: feature 4605

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.692`
- validation effect: `-0.669`
- test effect: `-0.641`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.729`

### Top natural activations

1. `act=1.3606` `token='▁Peut'`  
   Peut-être réussirai-je à comprendre ce cours en ligne.

2. `act=1.3606` `token='▁Peut'`  
   Peut-être qu’un jour, les villes lointaines ne seront plus un rêve inaccessible pour les enfants avides de liberté qui rêvent en regardant le ciel depuis leur balcon poussiéreux.

3. `act=1.3606` `token='▁Peut'`  
   Peut-être réussirai-je à comprendre ce cours s'il y a plus d'exemples concrets.

4. `act=1.3606` `token='▁Peut'`  
   Peut-on apprendre à chanter sans jamais entendre d'opéra ?

5. `act=1.3606` `token='▁Peut'`  
   Peut-être pourrait-elle chanter encore, mais elle préfère laisser les souvenirs reposer.

6. `act=1.3606` `token='▁Peut'`  
   Peut-être l'élève récitera-t-elle le poème avec passion.

7. `act=1.3606` `token='▁Peut'`  
   Peut-être serait-il bon que les élèves apprennent à manier à la fois le pinceau et l’encre de Chine.

8. `act=1.3606` `token='▁Peut'`  
   Peut-être a-t-il voyagé en Orient avant de devenir peintre.

---

# Variable 06: transitivity_valency

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 5382

- selection: `original_trainval_selected`
- train effect: `+0.939`
- validation effect: `+0.802`
- test effect: `+0.075`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.244`

### Top natural activations

1. `act=1.1373` `token='▁the'`  
   Could you please provide me with access to the latest policy documents on public education reform?

2. `act=1.1326` `token='▁the'`  
   Let me know if you need access to the data.

3. `act=1.1024` `token='▁the'`  
   Before students begin their research projects, they need to attend an orientation session where guidelines are explained, and after that, they must submit a proposal outlining their intended approach before being granted access to the library's restricted archives.

4. `act=1.0931` `token='▁the'`  
   If you're looking for something that's both healthy and satisfying, most people would probably say that homemade soups or stews tend to hit the spot, especially when it's cold outside and you need a warm, hearty meal to get you through the rest of the day.

5. `act=1.0928` `token='▁the'`  
   Here, once I finally caught up with her after what felt like hours of searching through the crowded festival, was my best friend Maria, beaming with excitement over her new job and barely listening to anything I had to say.

6. `act=1.0807` `token='▁the'`  
   If you wander through the old town at sunset, you'll find the galleries still open and eager to share their stories.

7. `act=1.0556` `token='▁the'`  
   I didn’t forget my ticket, but I still can't get through the gate without a stamp.

8. `act=1.0531` `token='▁the'`  
   Looking through the microscope, I saw a cell divide right there in the center of the slide.

## Candidate 2: feature 6102

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.918`
- validation effect: `-0.945`
- test effect: `-0.943`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.060`

### Top natural activations

1. `act=1.3908` `token='.'`  
   لقد صعدت الحافلة من الموقف الخارجي وانتظرت أن ينطلق المحرك.

2. `act=1.3894` `token='.'`  
   جاءت الجارة تسأل عن الضيف.

3. `act=1.3892` `token='.'`  
   بين الحين والآخر، نذهب إلى مكتبة المدينة التي تُدار من قبل ابن العم الذي يعيش في الطابق العلوي من نفس المبنى.

4. `act=1.3691` `token='.'`  
   أفادت شركة التكنولوجيا بتوظيف ستة موظفين جدد في مقرها الرئيسي خلال الشهر الماضي.

5. `act=1.3632` `token='.'`  
   في الوقت الذي غادر فيه عدد كبير من المسافرين المحطة الرئيسية بالقطار الصباحي المتجه إلى الجنوب، تأخر الركاب الآخرون بسبب خلل فني طرأ على القاطرة التابعة للقطار رقم 472 القادم من الشرق.

6. `act=1.3594` `token='.'`  
   بدأ خمسة موظفين العمل على تقرير الاجتماع الأسبوعي الذي طلب منه المدير في وقت مبكر من الصباح.

7. `act=1.3581` `token='.'`  
   يوجد جهازان في الصندوق.

8. `act=1.3527` `token='.'`  
   بعد أن اشتراها التذكرة، دخلت السيدة القطار وهي تحمل حقيبتها الصغيرة.

## Candidate 3: feature 164

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.919`
- validation effect: `+0.875`
- test effect: `+0.908`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.994`

### Top natural activations

1. `act=2.6237` `token='ولي'`  
   لقد قررت إدارة الشركة إشراك الموظفين في اجتماع يومي لتحسين التواصل وتحديد الأدوار والمسؤوليات بشكل أوضح حتى يشعر الجميع بأنهم جزء من الفريق ويتعاونوا على تحقيق الأهداف المشتركة بجدارة.

2. `act=2.6190` `token='▁بالأ'`  
   في مختبر بحثي متخصص في الذكاء الاصطناعي، قام الفريق العلمي بتطوير نموذج حسابي جديد يعتمد على بيانات تجريبية متعددة الأبعاد لتحسين الدقة في التنبؤ بالأنماط المعقدة.

3. `act=2.5554` `token='▁للأ'`  
   تحتاج المصاب بمرض السكري إلى مراقبة دقيقة لمستوى السكر في الدم، والذي يُقاس عادةً عبر استخدام جهاز قياس سكر الدم الرقمي الذي يوفر نتائج فورية ودقيقة يمكن الاعتماد عليها في ضبط الجرعات اليومية للأنسولين.

4. `act=2.5423` `token='▁بالأ'`  
   بينما كان الطالبون الصغار يتجولون في الغابة لجمع العينات النباتية، لاحظ أحدهم أن الأشجار الكبيرة التي تنمو بالقرب من مصدر المياه تبدو أكثر خضرة وصحة مقارنةً بالأشجار الأخرى البعيدة عن مصدر المياه، فاستفسر بفضول من مُعلّمه، الذي أجابه بأن الرطوبة المرتفعة والثروة المعدنية في التربة المجاورة للمياه تعزز نمو النباتات بشكل أكبر.

5. `act=2.5420` `token='▁بالأ'`  
   جاء الوالدان إلى غرفة الابن الصغير لتفقد حالته بعد أن أصيب برشة صدرية خفيفة بالأمس.

6. `act=2.5047` `token='▁ettikleri'`  
   Yerel bir okulda yürütülen etkileşimli coğrafya projesi sayesinde, öğrenciler şehirlerdeki ulaşım ağlarını incelediler, şehirler arası yolcu taşımalarını değerlendirdiler ve bu çalışmalar sırasında elde ettikleri bulguları hem kâğıt ortamında hem de bilgisayar destekli harita yazılımları üzerinden sunmaya çalıştılar.

7. `act=2.5038` `token='やっ'`  
   この間、田中さんの奥さんが家に遊びに来たとき、その子供たちがお手伝いをしてくれたのは本当にありがたかったんだよね、掃除も片付けもサッとやってくれて、ほんと助かった。

8. `act=2.4849` `token='▁ettikleri'`  
   Bir ilköğretim okulunda rehberlik hizmetleri kapsamında yeni uygulanan bir program sayesinde öğrencilerin kendi gelişim süreçlerini fark etmeleri ve bu farkındalığı derslerde elde ettikleri başarılarla ilişkilendirmeye başlamaları amaçlanmıştır.

## Candidate 4: feature 12059

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.911`
- validation effect: `-0.938`
- test effect: `-0.926`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.972`

### Top natural activations

1. `act=1.5565` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

2. `act=1.5565` `token='▁我們'`  
   我們明天早上七點出發。

3. `act=1.5565` `token='▁我們'`  
   我們馬上啟程去機場。

4. `act=1.2799` `token='▁Protect'`  
   Protect wetlands to preserve biodiversity.

5. `act=1.2627` `token='▁Voilà'`  
   Voilà le train, bruyant et bondé.

6. `act=1.2627` `token='▁Voilà'`  
   Voilà ce qu’on appelle un vrai cahotique de voyage, cette manière qu’a mon frère de toujours partir en road-trip sans préparer la moindre étape ni même jeter un œil à la météo.

7. `act=1.2627` `token='▁Voilà'`  
   Voilà donc le football, un sport exigeant et passionnant.

8. `act=1.2627` `token='▁Voilà'`  
   Voilà le itinéraire que nous avons choisi pour éviter les zones de travaux.

## Candidate 5: feature 4332

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.911`
- validation effect: `-0.938`
- test effect: `-0.926`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.962`

### Top natural activations

1. `act=1.9687` `token='▁그런데'`  
   그런데 이번엔 우리 팀이 이겼어요.

2. `act=1.9650` `token='▁Hola'`  
   Hola, ¿qué tal estás?

3. `act=1.9627` `token='▁그래'`  
   그래도 그렇게까지 했단 말이야?

4. `act=1.9627` `token='▁그래'`  
   그래도 이 일이 이렇게 잘 풀릴 줄은 몰랐어.

5. `act=1.9627` `token='▁그래'`  
   그래도 넌 여전히 아빠 같아.

6. `act=1.9627` `token='▁그래'`  
   그래도 이번 출장은 정말 놀랐어. 예상보다 훨씬 일이 순조로웠거든.

7. `act=1.9627` `token='▁그래'`  
   그래도 이 기계는 예전보다 훨씬 조용하네.

8. `act=1.9619` `token='▁İki'`  
   İkisinin de dikkatini çeken en tuhaf şey, ormanın derinliklerinden gelen ve aynı anda hem çığlık gibi hem de susuzluk çeken bir köynək sesi gibi duyan, onlarca kuşun birdenbire kafeslerine sığındığı ince hüzne benzer sesydi.

---

# Variable 07: voice_and_agent_prominence

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 8235

- selection: `original_trainval_selected`
- train effect: `+0.855`
- validation effect: `+0.921`
- test effect: `+0.623`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.657`

### Top natural activations

1. `act=1.6193` `token='mises'`  
   L’expérience montre que les premiers résultats obtenus par l’équipe confirment les hypothèses émises lors de la phase préliminaire.

2. `act=1.5880` `token='а'`  
   Според официални източници, отчетеният резултат от изследването относно състоянието на училищната инфраструктура в провинцията е в противоречие с информацията, предоставена преди месец от министерството на образованието.

3. `act=1.5412` `token='▁prises'`  
   Selon les premiers éléments d'information disponibles, le maire de la ville a confirmé, lors d'une conférence de presse hier soir, que plusieurs services municipaux auraient pu être impactés indirectement par les mesures prises en urgence par le gouvernement régional.

4. `act=1.5096` `token='▁données'`  
   Ces trois étudiants, qui ont tous suivi les mêmes cours et travaillé avec le même encadrement, ont rédigé leurs rapports en respectant scrupuleusement les consignes données.

5. `act=1.5040` `token='а'`  
   Според информацията, предоставена от началния ръководител, екипът трябва да се състои от шест човека.

6. `act=1.4934` `token='cidas'`  
   Cada estudiante del curso participó en al menos una de las tres actividades formativas ofrecidas.

7. `act=1.4873` `token='▁prises'`  
   Les mesures prises en faveur de la protection de l’environnement montrent clairement que tous les acteurs concernés s’engagent pleinement dans cette démarche écologique commune.

8. `act=1.4873` `token='▁prises'`  
   Les mesures prises par le gouvernement français visent à renforcer les protections sociales tout en maintenant l’équilibre des comptes publics, malgré les critiques exprimées par plusieurs partis politiques.

## Candidate 2: feature 10996

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.871`
- validation effect: `+0.909`
- test effect: `+0.225`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.643`

### Top natural activations

1. `act=1.0441` `token='▁be'`  
   Gizonek emazkira begiratuz esan zuenez, semea gaztelaraz aleak egin behar izan zituen.

2. `act=1.0436` `token='▁be'`  
   Dass die neuen Gesetze bereits in Kraft sind, merke ich erst, als ich vor ein paar Tagen versuchte, eine Gewerbeaufnahme zu beantragen und der Sachbearbeiter mir klar machte, dass sich die Voraussetzungen grundlegend geändert hätten.

3. `act=1.0433` `token='▁be'`  
   Kami sedang merencanakan kunjungan ke kantor gubernur besok pagi untuk menyampaikan aspirasi warga mengenai akses pendidikan yang masih terbatas di daerah pelosok.

4. `act=1.0379` `token='▁be'`  
   A single delayed flight has caused several hundred passengers to miss their connecting departures, stranding a large number of travelers at the international airport until further arrangements can be made.

5. `act=1.0287` `token='▁be'`  
   Kami berdua harus menghadiri rapat manajemen besok pagi.

6. `act=1.0253` `token='▁be'`  
   Zehar karpeta begiratzen hasi zen gero, kanpoko argian pilota jokatzea ez zuen asmatu, eta bertan amak ahal den laster itzuli behar izan zuen laguntzeko.

7. `act=1.0152` `token='▁be'`  
   Kami sedang merencanakan makan malam bersama di rumah nenek besok sore, jadi semua orang harus datang termasuk kakek yang baru pulang dari berobat pagi tadi.

8. `act=1.0072` `token='▁be'`  
   Kami sedang merencanakan keberangkatan tim ke lokasi proyek besok pagi pukul tujuh menggunakan bus yang telah dipesan perusahaan.

## Candidate 3: feature 12096

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.907`
- validation effect: `+0.961`
- test effect: `+0.685`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.454`

### Top natural activations

1. `act=1.3627` `token='▁rempli'`  
   Le train à grande vitesse qui traversait la vallée ensoleillée était rempli de touristes venus admirer le paysage pittoresque des montagnes recouvertes de neige.

2. `act=1.3615` `token='▁salu'`  
   Monsieur le Président, votre discours a été salué comme un appel à l'unité nationale.

3. `act=1.3482` `token='▁intense'`  
   While the team's training schedule was intense and demanding, their dedication during practice sessions contrasted sharply with the casual attitude they displayed during actual matches.

4. `act=1.3274` `token='▁angemessen'`  
   Wäre das Projekt angemessen finanziert worden, stünden die Chancen gut, dass die Forschungsergebnisse bis zum Ende des Sommers veröffentlicht werden könnten.

5. `act=1.2988` `token='füllt'`  
   Der Bus, den wir genommen haben, war überfüllt.

6. `act=1.2977` `token='schädig'`  
   Die Maschine ist beschädigt worden.

7. `act=1.2922` `token='schädig'`  
   Die Wand war durch den Sturz beschädigt.

8. `act=1.2898` `token='▁intense'`  
   She said the game was intense until the final whistle, but now we're all back here wondering how it could have gone so differently.

## Candidate 4: feature 2491

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.955`
- validation effect: `+0.990`
- test effect: `+0.696`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.428`

### Top natural activations

1. `act=1.2007` `token='▁war'`  
   Als ich durch den schattigen Wald spazierte, war die Stille bereits vom fernen Donnergrollen unterbrochen worden, und die Blätter, vom Regen gebeugt, zeigten deutlich, dass ein heftiges Unwetter vorübergezogen sein musste.

2. `act=1.1944` `token='▁war'`  
   Als ich gestern Abend nach Hause kam, war meine Schwester gerade dabei, das Abendessen vorzubereiten, und fragte mich, ob ich heute Nachmittag mit zum Einkaufen kommen würde, weil sie für nächsten Sonntag einen gemütlichen Braten kochen wollte.

3. `act=1.1852` `token='▁war'`  
   Als ich in die Küche kam, war das Gericht bereits fertig, nur der Salat fehlte noch, den hatte sie extra für mich frisch zubereitet.

4. `act=1.1462` `token='▁war'`  
   Als ich am frühen Morgen die Wohnung verließ, war der Himmel noch grau und kalt, doch mittags brannte bereits die Sonne hell vom wolkenlosen Himmel, sodass ich beschloss, spazieren zu gehen, um die wärmere Luft zu genießen, während die Katze friedlich auf der Terrasse schlief und der Wind sanft durch die Blumen im Beet wehte.

5. `act=1.1443` `token='▁war'`  
   Als wir in den Zug nach München stiegen, warfen wir noch einen Blick auf die Karte, um zu prüfen, welche Haltestelle uns am schnellsten zum Stadtzentrum bringen würde.

6. `act=1.1421` `token='▁war'`  
   Weil es den ganzen Tag geregnet hat, war der Fluss am späten Abend viel höher als gewöhnlich.

7. `act=1.1305` `token='▁war'`  
   Als der Arzt die Ergebnisse der Blutuntersuchungen sah, war er sich fast sicher, dass die Symptome auf eine chronische Entzündung zurückgingen, obwohl er noch weitere Tests vorschlagen wollte, um jede andere Möglichkeit auszuschließen.

8. `act=1.1260` `token='▁war'`  
   Als er endlich ins Bett fiel, war die Müdigkeit fast wie ein sanfter Schlaftrunk.

## Candidate 5: feature 10398

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.930`
- validation effect: `+0.960`
- test effect: `+0.691`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.419`

### Top natural activations

1. `act=1.8618` `token='▁will'`  
   They had been baking the bread since dawn, yet it will not be ready until after the sunset.

2. `act=1.8186` `token='▁will'`  
   I have noticed that whenever my mother bakes a batch of her famous cinnamon rolls, she always makes twice as many as needed, so there will certainly be plenty left for everyone in the house, including those who might not even be home yet but are expected for dinner.

3. `act=1.7879` `token='▁will'`  
   The mayor announced at the press conference that, "We will implement new policies to improve public transportation by next summer," which drew applause from the audience.

4. `act=1.7864` `token='▁will'`  
   The manager reviewed the report yesterday and will present it at the meeting today.

5. `act=1.7716` `token='▁will'`  
   The mayor announced at the press conference, "We will hold a public meeting next week to address the concerns about the new development."

6. `act=1.7457` `token='▁will'`  
   It’s definitely true that she will attend the meeting if we confirm her schedule by noon, so we should send the official invitation right away and let her know how important her presence is for the discussion.

7. `act=1.7382` `token='▁will'`  
   He explained the theory yesterday and will continue today, moving through each stage clearly.

8. `act=1.7321` `token='▁will'`  
   The train left the station on time and will arrive at the next city just before sunset.

---

# Variable 08: causativity_and_valency_change

- Original SAE evidence tier: **B1**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 8182

- selection: `original_trainval_selected`
- train effect: `+0.894`
- validation effect: `+0.934`
- test effect: `+0.783`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.993`

### Top natural activations

1. `act=4.0564` `token='▁intens'`  
   Per quanto avesse già espresso chiaramente la sua opinione durante la discussione del pittore e della sua ultima mostra, non si oppose quando lei riprese a parlare con entusiasmo del suo stile particolare e della sua capacità di evocare emozioni profonde con pennellate decise e colori intensi.

2. `act=3.9766` `token='▁bien'`  
   La pâte à tarte faite maison, qu'on prépare en mélangeant soigneusement la farine, le beurre froid coupé en petits morceaux et un peu de sel dans une jatte creuse, est délicatement étalée sur une plaque bien huilée avant d'être fourrée.

3. `act=3.9512` `token='اقتصادية'`  
   في ظل التطورات السريعة في علوم الحاسوب، تُظهر الخوارزميات الحديثة قدرات عالية على معالجة البيانات الضخمة بسرعة وإتقان، مما يمكّن الباحثين من اكتشاف نماذج معقدة تساعد في فهم دقيق للظواهر الطبيعية والاجتماعية والاقتصادية.

4. `act=3.9477` `token='▁chaude'`  
   Hier, j’ai peint le salon pendant que les enfants regardaient un film, et comme il faisait froid dans la pièce, j’ai allumé le radiateur et je me suis mise à rôder avec une couverture, car tout en travaillant, je grelottais un peu, même si j’avais mis une veste chaude avant de commencer.

5. `act=3.9310` `token='▁stable'`  
   Le père, qui était généralement réservé et peu enclin à exprimer ses sentiments, a fini par admettre, après de longues heures de conversation avec son fils aîné, que leur relation avait évolué au fil des ans vers quelque chose de plus profond et de plus stable qu’il n’aurait jamais imaginé possible.

6. `act=3.9239` `token='ológicos'`  
   Resulta curioso cómo la manera en que el verbo se flexiona para mostrar el participio en los compuestos derivados —como en "corredor" o "jugador"— mantiene una cohesión semántica con el sustantivo al que se le agrega, a pesar de que ambas partes lleguen al mismo resultado por caminos morfológicos diferentes.

7. `act=3.9135` `token='▁leche'`  
   Mientras preparábamos la cena en casa de mis padres, mi hermana empezó a reírse al ver que el gato había derramado la leche del recipiente en el que lo dejaba para él, y comenté que, aunque eso significaba que tendríamos que limpiar antes de sentarnos a comer, era una pequeña alegría tener un animal que disfrutara tanto con algo tan simple como un poco de leche fresca.

8. `act=3.9056` `token='▁leche'`  
   El hermano de mi prima, que es muy apasionado por el cine clásico, organizó una proyección en la casa grande de su abuela para toda la familia y llevó también un enorme cartel hecho a mano con el nombre del film escrito en letra cursiva y adornado con dibujos, mientras las tías se sentaban en las sillas del jardín y los primos correteaban entre las mesas pidiendo galletas con leche.

## Candidate 2: feature 16378

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.873`
- validation effect: `-0.926`
- test effect: `-0.839`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.971`

### Top natural activations

1. `act=1.7051` `token='.'`  
   Bicycles line the street outside the community college, waiting for students who never arrive.

2. `act=1.6770` `token='.'`  
   Il faut absolument que vous vérifiiez vos réservations avant d'arriver à l'hôtel.

3. `act=1.6762` `token='.'`  
   S'il te plaît, éteins la télévision avant de commencer à dîner.

4. `act=1.6724` `token='.'`  
   Los niños en esta comunidad suelen ir a la escuela caminando todos los días.

5. `act=1.6679` `token='.'`  
   Follow the map instructions carefully.

6. `act=1.6506` `token='.'`  
   At a typical office, you'll find that managers often rely on team meetings to maintain communication.

7. `act=1.6492` `token='.'`  
   سافر الجند إلى المدينة بسرعة.

8. `act=1.6438` `token='.'`  
   Non ci sono alternative alla prenotazione online, se non si va di fretta.

## Candidate 3: feature 4441

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.863`
- validation effect: `+0.882`
- test effect: `+0.797`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.970`

### Top natural activations

1. `act=5.1045` `token='र्थ'`  
   विद्यार्थियों के सीखने की प्रक्रिया को सुगम बनाने के लिए अध्यापक को न केवल अपने विषय की गहराई से जानकारी होनी चाहिए, बल्कि उन्हें विद्यार्थियों के सीखने के तरीकों और उनकी आवश्यकताओं को भी समझना चाहिए।

2. `act=5.0552` `token='हर'`  
   महाकाव्य रामायण के नाटकीय अंकगणित के माध्यम से, विश्व के लोकप्रिय संस्कृति में भारतीय धर्म और नैतिकता के जटिल विचारों के संवाद की गहराई और विशालता को अवश्य ध्यान देना चाहिए।

3. `act=5.0130` `token='हर'`  
   आधुनिक विज्ञान और प्रौद्योगिकी के क्षेत्र में प्रगति के साथ, मानव अंतरिक्ष यात्रा और कृत्रिम बुद्धिमत्ता जैसे क्षेत्र अब अधिक उन्नत हो रहे हैं और हमारे जीवन को गहराई से प्रभावित कर रहे हैं।

4. `act=4.8856` `token='ய'`  
   இன்றைய மாலை நிகழ்ச்சியில், குடியரசுத் தலைவரின் அறிக்கையை விரிவாக ஆராய நாம் முடிவு செய்திருக்கிறோம், அதற்கு முன்பாக இந்த நிகழ்ச்சியில் பங்கேற்றுள்ள குடியரசுத் தலைவருடன் நாம் பேசினோம்.

5. `act=4.8848` `token='हर'`  
   आधुनिक विज्ञान और प्रौद्योगिकी के क्षेत्र में तेजी से विकास हो रहा है, जिससे नए अविष्कार और आविष्कार लगातार हो रहे हैं, जो आम जनजीवन को गहराई से प्रभावित कर रहे हैं।

6. `act=4.8531` `token='ंघ'`  
   नए नियमों के लागू होने के बाद से नागरिकों के बीच चिंता का माहौल है, क्योंकि अधिकारियों का कहना है कि ये नियम देश के सुरक्षा खतरों को कम करने के लिए आवश्यक हैं, जबकि विपक्ष इन्हें अत्यधिक और नागरिक अधिकारों के उल्लंघन के रूप में देख रहा है।

7. `act=4.7889` `token='▁ritm'`  
   Birçok veli, okul müdürlerine sorunlarını dile getirmek ve çocuklarının derslerindeki eksikliklerin farkında olmalarını sağlamak için düzenli olarak toplantılar yaparken, öğretmenler de sınıf içi uygulamalarda farklı yaklaşımlar benimseyerek her öğrencinin öğrenme ritmini dikkate almaya çalışıyor.

8. `act=4.7526` `token='▁durabil'`  
   Genel müdür, bizim Ankara'dan Karabük'e olan yolculuğumuz sırasında şunu sordu: "İstanbul'dan geçerken eski şoförümüzle bir kahve içip durabilir miyiz?"

## Candidate 4: feature 7247

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.870`
- validation effect: `-0.940`
- test effect: `-0.853`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.965`

### Top natural activations

1. `act=1.6231` `token=','`  
   Lei mi ha telefonato mentre ero fuori, ma non ho risposto.

2. `act=1.6155` `token=','`  
   Вчера мы закончили тренировку рано, так как решили повторить материал уже сегодня вечером.

3. `act=1.6108` `token=','`  
   Я пришёл на работу рано, чтобы успеть подготовить документы к встрече с клиентом.

4. `act=1.6093` `token=','`  
   Вчера я закончила работу рано, потому что всё успела сделать к обеду.

5. `act=1.5922` `token=','`  
   No tomaba medicamentos desde hacía semanas, pero su fiebre persistía igual.

6. `act=1.5901` `token=','`  
   Пироги с капустой я испёк ещё вчера, а сейчас уже все съели.

7. `act=1.5864` `token=','`  
   Сергей още работеше по проекта си отпреди месец, когато босът го повика в кабинета.

8. `act=1.5838` `token=','`  
   Вчера мы закончили проект вовремя, и сегодня начали обсуждать новый заказ с клиентом.

## Candidate 5: feature 164

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.918`
- validation effect: `+0.938`
- test effect: `+0.866`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.992`

### Top natural activations

1. `act=2.6237` `token='ولي'`  
   لقد قررت إدارة الشركة إشراك الموظفين في اجتماع يومي لتحسين التواصل وتحديد الأدوار والمسؤوليات بشكل أوضح حتى يشعر الجميع بأنهم جزء من الفريق ويتعاونوا على تحقيق الأهداف المشتركة بجدارة.

2. `act=2.6190` `token='▁بالأ'`  
   في مختبر بحثي متخصص في الذكاء الاصطناعي، قام الفريق العلمي بتطوير نموذج حسابي جديد يعتمد على بيانات تجريبية متعددة الأبعاد لتحسين الدقة في التنبؤ بالأنماط المعقدة.

3. `act=2.5554` `token='▁للأ'`  
   تحتاج المصاب بمرض السكري إلى مراقبة دقيقة لمستوى السكر في الدم، والذي يُقاس عادةً عبر استخدام جهاز قياس سكر الدم الرقمي الذي يوفر نتائج فورية ودقيقة يمكن الاعتماد عليها في ضبط الجرعات اليومية للأنسولين.

4. `act=2.5423` `token='▁بالأ'`  
   بينما كان الطالبون الصغار يتجولون في الغابة لجمع العينات النباتية، لاحظ أحدهم أن الأشجار الكبيرة التي تنمو بالقرب من مصدر المياه تبدو أكثر خضرة وصحة مقارنةً بالأشجار الأخرى البعيدة عن مصدر المياه، فاستفسر بفضول من مُعلّمه، الذي أجابه بأن الرطوبة المرتفعة والثروة المعدنية في التربة المجاورة للمياه تعزز نمو النباتات بشكل أكبر.

5. `act=2.5420` `token='▁بالأ'`  
   جاء الوالدان إلى غرفة الابن الصغير لتفقد حالته بعد أن أصيب برشة صدرية خفيفة بالأمس.

6. `act=2.5047` `token='▁ettikleri'`  
   Yerel bir okulda yürütülen etkileşimli coğrafya projesi sayesinde, öğrenciler şehirlerdeki ulaşım ağlarını incelediler, şehirler arası yolcu taşımalarını değerlendirdiler ve bu çalışmalar sırasında elde ettikleri bulguları hem kâğıt ortamında hem de bilgisayar destekli harita yazılımları üzerinden sunmaya çalıştılar.

7. `act=2.5038` `token='やっ'`  
   この間、田中さんの奥さんが家に遊びに来たとき、その子供たちがお手伝いをしてくれたのは本当にありがたかったんだよね、掃除も片付けもサッとやってくれて、ほんと助かった。

8. `act=2.4849` `token='▁ettikleri'`  
   Bir ilköğretim okulunda rehberlik hizmetleri kapsamında yeni uygulanan bir program sayesinde öğrencilerin kendi gelişim süreçlerini fark etmeleri ve bu farkındalığı derslerde elde ettikleri başarılarla ilişkilendirmeye başlamaları amaçlanmıştır.

---

# Variable 09: analytic_vs_synthetic_encoding

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 6579

- selection: `original_trainval_selected`
- train effect: `-0.502`
- validation effect: `-0.561`
- test effect: `-0.480`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.550`

### Top natural activations

1. `act=1.0670` `token='▁içeri'`  
   Uçak pistte beklerken yolcular içeriye yönlendiriliyordu.

2. `act=1.0104` `token='▁içeri'`  
   Komşunun içeri girdiğini duydukça kapımı araladım.

3. `act=1.0025` `token='▁içeri'`  
   Taksi şoförü yolcularına konforlu ve güvenli bir seyahat vaat ederken hem içeri hem de dışarıya dikkat etmek zorunda.

4. `act=0.9950` `token='▁içeri'`  
   Herhangi bir futbol mağazasına girdiğinizde karşısınıza çıkan oyun kıyafetleri, çantalar ya da spor ayakkabıları genellikle marka rehberiyle değil, içeriğe ve kullanıma uygunluklarına göre seçilen ürünlerdir.

5. `act=0.9945` `token='▁içeri'`  
   Otobüsle şehir merkezine vardığında kapısını açan yolcu, içeriye girerken bastırdığı çantayı uzunca yolda taşıyacağını fark etti.

6. `act=0.9832` `token='▁içeri'`  
   Kapıya vardığında içerideki televizyonun sesi hâlâ açık, odada biraz karanlık olsa da ışıklar sönmüştü.

7. `act=0.9827` `token='▁içeri'`  
   Parkta eski aile dostunu görünce içeri girmek istedim ama annemle tartıştığımız için kapıya bile yaklaşmadım.

8. `act=0.9765` `token='▁içeri'`  
   Geldiğinde bize bakmadan içeri girdi.

## Candidate 2: feature 144

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.507`
- validation effect: `-0.728`
- test effect: `-0.570`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.528`

### Top natural activations

1. `act=1.1842` `token='▁को'`  
   माँ ने अपनी नातिन को पसंद का संगीत बजाकर मन को शांति दिलाया।

2. `act=1.1087` `token='▁में'`  
   उसने अपने दोस्त को एक सुंदर छोटी कहानी कहकर उसके मन में आशा ला दी।

3. `act=1.1029` `token='▁में'`  
   मंदिर के शिल्पकला सजाये हुए गुंबद को देखकर मन में एक अनोखी शांति छा गई।

4. `act=1.0491` `token='▁में'`  
   उस महान कलाकार ने अपनी फिल्म में पारंपरिक रूप से गाड़ा हुआ प्रेम तथा दुख के साथ समझौता करते हुए दर्शकों के दिल में एक अद्वितीय भावनात्मक आभा

5. `act=1.0453` `token='▁को'`  
   खूबसूरत पक्षियों के डालियों पर बैठे हुए सूरज की किरणें झाकते हुए खेत के हरे भरे फलदार पेड़ मन को आनंदित कर रहे हैं।

6. `act=1.0277` `token='▁में'`  
   वह अध्यापिका कहानी सुनाते हुए छात्रों के मन में चित्र बना देती है।

7. `act=1.0228` `token='▁को'`  
   पहाड़ियों के ऊपर सुबह की जलवायु में बिछा हुआ सफेद धुंआ मन को शांत करता है और प्रकृति के आलोक की ओर एक नई प्रेरणा लाता है।

8. `act=1.0172` `token='▁को'`  
   मैंने उस कलाकार की पेंटिंग देखी, जिसके रंगों के मिश्रण ने सचमुच मेरे मन को झंझोड़ा दे दिया।

## Candidate 3: feature 4222

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.654`
- validation effect: `-0.028`
- test effect: `-0.651`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.133`

### Top natural activations

1. `act=1.4186` `token='▁di'`  
   L'allenatore ha detto ai giocatori che, se non avessero migliorato la loro forma fisica, non sarebbero stati schierati neanche per l'amichevole di fine mese.

2. `act=1.3701` `token='▁de'`  
   Cuando mi hermana terminó de arreglar el jardín trasero para la fiesta de fútbol de los niños, noté que se había olvidado de cortar el césped detrás del balancín rojo.

3. `act=1.3449` `token='▁de'`  
   Es posible que, al ver el menú de la cena de hoy, concluyéramos que con las frutas de temporada y las legumbres frescas, podría salir algo muy rico y saludable, aunque también dependa del criterio de cada uno sobre lo que se considera bien cocinado.

4. `act=1.3401` `token='▁de'`  
   Anoche pinté el cuadro que quería para la fiesta de mañana.

5. `act=1.3303` `token='▁de'`  
   Mientras mi hermana decoraba el salón para la fiesta de cumpleaños, yo preparaba los postres que había elegido la semana anterior.

6. `act=1.3118` `token='▁de'`  
   En el partido de fútbol de ayer, el delantero corrió sin marcas por el centro del campo y anotó un gol desde fuera del área sin que nadie lo viera venir.

7. `act=1.2914` `token='▁de'`  
   Las porterías fueron rematadas con fuerza durante el amistoso de fútbol entre los dos equipos nacionales.

8. `act=1.2817` `token='▁del'`  
   Durante el festival del cine de Salud y Vida Natural en Málaga, un documentalista mostró una película que exploraba los múltiples beneficios del yoga tradicional sobre la salud mental, emocional y física de los adultos mayores.

## Candidate 4: feature 6379

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.554`
- validation effect: `-0.156`
- test effect: `-0.509`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.092`

### Top natural activations

1. `act=1.3801` `token='▁rapport'`  
   In many workplaces, employees regularly exchange informal greetings to build rapport.

2. `act=1.2776` `token='ification'`  
   Given the contextual indicators in the conversation thread, it seems likely that the user intended to request clarification on the project timeline.

3. `act=1.2543` `token='y'`  
   Kindergarten teachers often spend hours preparing creative activities that spark curiosity in young children.

4. `act=1.2439` `token='▁help'`  
   If you're feeling unwell while traveling, seek medical help immediately.

5. `act=1.2438` `token='▁conflict'`  
   In family therapy sessions, the therapist often emphasizes how parents can reframe their perspectives so that children's actions are seen as expressions of unmet needs rather than deliberate attempts to provoke conflict.

6. `act=1.2152` `token='▁comfort'`  
   After years of drifting apart, her sudden return into his life felt like an old door creaking open once more, revealing how deeply they had both changed, yet still managed to find comfort in their shared past.

7. `act=1.2136` `token='▁Hoffnung'`  
   Seine Erzählung über die Heilung der Dörfer brachte Hoffnung in das kranke Dorf.

8. `act=1.2011` `token='▁guidance'`  
   As the instructor circled the classroom, she watched each student working carefully through the complex math problems on their worksheets, offering quiet guidance and encouragement when needed.

## Candidate 5: feature 10578

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.506`
- validation effect: `-0.141`
- test effect: `-0.385`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.945`

### Top natural activations

1. `act=1.4284` `token='▁on'`  
   All the kids on the bus seemed to have packed their backpacks together.

2. `act=1.3235` `token='▁in'`  
   All the birds in the flock flew together across the sky.

3. `act=1.3235` `token='▁in'`  
   All the birds in the flock flew low across the field, seemingly determined to stir up every last seed from the ground before the rain came.

4. `act=1.3235` `token='▁in'`  
   All the birds in the garden flew up together when the cat jumped into the bushes.

5. `act=1.2990` `token='▁in'`  
   All the kids in the camp gathered around the bonfire to share stories.

6. `act=1.2659` `token='▁on'`  
   All the players on the team signed the autograph book after the final game.

7. `act=1.2659` `token='▁on'`  
   All the players on the team practiced together without any exceptions.

8. `act=1.2275` `token='▁в'`  
   Хората в регионът започнаха да се притесняват заради рязкия щурец на температурите през зимата.

---

# Variable 10: morphological_segmentation_type

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.983**

## Candidate 1: feature 6125

- selection: `original_trainval_selected`
- train effect: `-0.708`
- validation effect: `-0.531`
- test effect: `-0.456`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `5.115`

### Top natural activations

1. `act=0.6737` `token='▁İstanbul'`  
   Bu yıl İstanbul Sanat Fuarı’nda tanınmış bir sanatçının yapımı olan resimler defalarca özel koleksiyonlara satışa çıkarıldı ve koleksiyoncular arasında büyük ilgiyle karşılandı.

2. `act=0.6644` `token='▁İstanbul'`  
   Ah, bu tür bir sanat sergisi İstanbul'da açılıyor diye duymak inanılmaz bir sürpriz oldu, hem de bu kadar kısa süre içinde hazırlayabilmek çok etkileyiciydi!

3. `act=0.6269` `token='tkinlik'`  
   Parktaki Etkinlik #2024YazProjesi ile devam ediyor.

4. `act=0.6190` `token='▁İstanbul'`  
   Günün bir yerinde İstanbul’a vardığımı hatırlıyorum ama yolculuk çok uzun sürdü.

5. `act=0.6187` `token='▁İstanbul'`  
   Taksi sürücüsü İstanbul’un her zamanki gibi kalabalık ve hareketli caddelerinde 20 turuncu renkli minibüsün yolcu almak için beklediği yerden geçenleri dikkatle izlerken, biraz geride duran polis memuru adeta bu olaya bir turist gibi ilgiyle bakıyordu.

6. `act=0.6172` `token='▁İstanbul'`  
   Annesiyle annem bu sabah İstanbul’a uçakla geldiklerini söylemiş ama neden tam o zaman gelip bizimle birlikte kahvaltı yapmadıklarını hâlâ anlamadım.

7. `act=0.6148` `token='▁İstanbul'`  
   Dayımların oğlu İstanbul'da bir bilgisayar mühendisliği mezunu olduğunu belirterek, bizim aileyle kalıcı bağ kurmak için Konya'ya taşındığını ve şimdi ailenin bu yeni durumu hakkında konuşmalar yaptığını anlattı.

8. `act=0.6137` `token='▁İstanbul'`  
   Otomobilimiz İstanbul’a varmak için yol aldı.

## Candidate 2: feature 15843

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.731`
- validation effect: `+0.335`
- test effect: `+0.704`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.162`

### Top natural activations

1. `act=1.6384` `token='mız'`  
   Eğer biriyle olan arkadaşlığımız dün gece yemeğe çıkmaz olsaydı derinleşemezdi ama artık bu bağlar kuvvetlenmeye devam ediyor.

2. `act=1.6258` `token='m'`  
   Kuzeni, doğum günümde bana bir hediye getirmek yerine onu babamın evinden almamı istedi.

3. `act=1.6179` `token='m'`  
   Her hafta birlikte resim sergilerine katılmak, onlarla sohbet etmek ve sanatı konuşmak, kavga etmeden dostluğumuzun uzun süre devam etmesini sağlamıştı.

4. `act=1.6018` `token='m'`  
   Annesiyle geçirdiğimiz zamanlar çocukluğumdaki en güzel anılardan biridir.

5. `act=1.5775` `token='m'`  
   Çocuğunu almak için sadece on dakika zamanım vardı.

6. `act=1.5769` `token='m'`  
   Asla bu tür bir sorumluluk almadım, çünkü uzmanlık alanım başka yerde.

7. `act=1.5625` `token='m'`  
   Küçük bir toplantıda konuşurken cümlem herkesi etkiledi ama konuşmamın ardından onları memnun edebilmek için daha fazla detay eklemem gerektiğine karar verdim.

8. `act=1.5621` `token='m'`  
   Parkta yürüyen yaşlı adam turistlerden biriyle şöyle dediğini duydum: “Bu sokaklar çocukluğumdaki kadar yeşil değil, ama hâlâ sabahları neşeyle dolu.”

## Candidate 3: feature 8119

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.732`
- validation effect: `-0.643`
- test effect: `-0.029`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.064`

### Top natural activations

1. `act=0.8440` `token='▁рек'`  
   На работе мне пришлось повторно проверить документ, который принёс коллега из соседнего кабинета, чтобы убедиться, что все подписи и реквизиты указаны правильно и без пропусков.

2. `act=0.8001` `token='▁alan'`  
   Bilim kampında araştırma ekibi halen veri toplamakta ve alan ölçümlerini kaydediyor.

3. `act=0.7976` `token='▁alan'`  
   Daha önce duymadığım bu teori, alan çalışmasında çarpıcı bir yenilik olarak öne çıkıyor.

4. `act=0.7810` `token='▁dal'`  
   Resim, kırmızı-lacivert dalgalarla kaplı bir kıyı manzarasıydı.

5. `act=0.7555` `token='▁alan'`  
   Bu arada, hocalarımızın dediği gibi, derslerin her biri aynı derecede önemlidir ve hepsinden ziyade matematikle Türkçe'ye verilen zaman yeterince uzun olmalıdır, çünkü öğrencilerin hem düşünme yetenekleri hem de ifade kabiliyetleri bu iki alanla geliyor.

6. `act=0.7392` `token='▁alan'`  
   Köyde geçen yıl kurulan rüzgar jeneratörleri, hem enerji üretimini artırdı hem de doğal yaşam alanlarını etkiledi.

7. `act=0.7276` `token='▁рек'`  
   Сестра сделала ректальный клизм.

8. `act=0.7254` `token='▁dal'`  
   Çocuklar bahçede koşarken birkaç kuş dalda konuşmaya devam etti.

## Candidate 4: feature 16361

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.797`
- validation effect: `-0.556`
- test effect: `-0.443`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.037`

### Top natural activations

1. `act=1.2998` `token='▁नाम'`  
   डॉक्टर ने मेरी बिमारी का नाम सुनाया।

2. `act=1.2464` `token='▁नाम'`  
   किताब के मुखपृष्ठ पर छात्र का नाम स्पष्ट रूप से लिखा हुआ था।

3. `act=1.2458` `token='▁नाम'`  
   मेरी दादी हमेशा कहती रहती थीं कि पड़ोस में रहने वाला नन्हा कुत्ता, जिसका नाम मोमो है, हमारे घर के सभी बच्चों के साथ बड़ा खेलता है और वो भी

4. `act=1.2114` `token='▁नाम'`  
   पोस्टर पर उसका नाम छापा हुआ था।

5. `act=1.1943` `token='▁नाम'`  
   मैंने उसे अपना नाम लिखवाया।

6. `act=1.1912` `token='▁नाम'`  
   माँ ने बच्चे को पेड़ का नाम बताया।

7. `act=1.1457` `token='▁नाम'`  
   पेड़ की छाँव में बैठकर उसने अपने पुत्र को सब्जियों का नाम बताते हुए सुना।

8. `act=1.1357` `token='▁नाम'`  
   इलेक्ट्रॉन का नाम सुनकर विज्ञानी महिला खुश हो गई।

## Candidate 5: feature 14319

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.717`
- validation effect: `-0.455`
- test effect: `-0.404`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.994`

### Top natural activations

1. `act=2.2692` `token='ِ'`  
   صُدِرَ الحرفُ من قلبِ صديقتي بِوُضوحٍ.

2. `act=2.1936` `token='ِ'`  
   رَأَيْتُ فِي مَكْتَبِهَا طَاقِمَ عَمَلٍ مَرْتَفِعَ الدَّرَجَةِ يَتَحَدَّثُونَ عَنْ تَقْنِيَّاتٍ جَدِيدَةٍ أَثْنَاءَ اجْتِمَاعٍ صَبَاحِيٍّ مُعَكَّس

3. `act=2.1810` `token='ِ'`  
   ضَعِّفْ الزَّيتَ الزيتونِيَ في الحَفْرَةِ ودُلّنِي بِالحَمِيصِ المُحَلّى بِالمَعْدِنِي.

4. `act=2.1810` `token='ِ'`  
   رأيتُ طالبَيْ جامعتِنا اللذينِ تعلّما معاً منذ ثلاث سنواتٍ يُقدّمان محاضرَتَيْ تخرّجِهِم في قاعةٍ مليئةٍ بالحضور، ما زالا يظهِران فخورَيْنِ بلُقائِهنَا اليوم وهم ينتظِران تصفيقَ الجماهيرِ المُتحمسةِ لهما.

5. `act=2.1772` `token='ِ'`  
   حَضَرَتْ الجَمَاعَةُ المَجْلِسَ بِالْوُضُوعِ الْخَاصَّةِ بِالتَّعَارُفِ مُبَكِّرًا.

6. `act=2.1750` `token='ِ'`  
   باتَساقطُ الأمطارُ على الوِرْدَةِ فِي الحديقةِ الصغيرةِ عندَ بابِ المنزلِ، أحسَّتُ برائحةٍ عطرةٍ مألوفةٍ تذكِّرُني بطفولتيِ وحقلِ الزهورِ الذي كان يُحيطُ ببيتي.

7. `act=2.1748` `token='ِ'`  
   رَسَمَ الرُّوحُ الأُنَاسِيُّ صُورَةً لِلأَبِ وَالبِنْتِ جالِسَيْنِ فِي حَدِيقَةٍ خَضْرَاءَ بَيْنَ أَشْجَارٍ كَثِيفَةٍ.

8. `act=2.1638` `token='ِ'`  
   رُبَّمَا نَجِدُ فِي الصُّحُفِ تَقْلِيدًا لِلتَّفَاعُلَاتِ الْأُمَّيَّةِ، بَلْ يَكُونُ هَذَا أَمْرًا مُؤَثِّرًا فِيمَا يَقُومُ بِهِ النَّاسُ فِي مُجَالِ الْعَمَلِ الْجَمَ

---

# Variable 11: agreement_indexing_density

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.762**

## Candidate 1: feature 758

- selection: `original_trainval_selected`
- train effect: `+0.826`
- validation effect: `+0.818`
- test effect: `+0.673`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.677`

### Top natural activations

1. `act=1.8855` `token='illé'`  
   La femme biologiste a observé avec attention les oiseaux migrateurs qui s’abritaient dans la forêt humide et comment leurs chants changes s’accordaient parfaitement avec le murmure du vent léger et des feuilles mouillées par l'humidité matinale.

2. `act=1.8851` `token='rea'`  
   Es muy probable que el tren haya llegado con retraso debido a los fuertes vientos que afectaron las líneas férreas cercanas a la estación principal de la ciudad.

3. `act=1.8141` `token='▁vivo'`  
   A pesar de que a veces me siento como un mueble viejo en la sala de mi casa, esperando sin hacer ruido que alguien me preste atención, también sé que, al igual que los seres vivos, una mesa bien usada puede tener tanto historia y valor emocional como una persona callada pero observadora.

4. `act=1.8010` `token='ólica'`  
   Es indudable que la influencia del surrealismo en el cine latinoamericano es profunda y claramente perceptible en la narrativa onírica de directoras como Lucrecia Martel o en las representaciones simbólicas de los paisajes nacionales.

5. `act=1.7997` `token='▁passé'`  
   Tous les membres de la famille, rassemblés pour célébrer le mariage de leur nièce, ont participé ensemble à une danse traditionnelle qui transmettait les valeurs et les rythmes hérités des générations passées.

6. `act=1.7771` `token='▁passé'`  
   Chez certaines familles de la vieille noblesse bretonne, on continue de transmettre d'anciens chants et contes aux enfants autour du feu, comme si le temps s'était figé dans l'harmonie des générations passées.

7. `act=1.7667` `token='▁masculino'`  
   El jefe de la oficina principal invitó a sus colegas femeninas y a sus ayudantes masculinos a una reunión informal para discutir el nuevo proyecto y escuchar sus opiniones sobre los plazos y las estrategias sugeridas por el departamento comercial.

8. `act=1.7455` `token='▁masculina'`  
   La directora del colegio anunció que se han incrementado las matrículas femeninas y masculinas en la escuela secundaria.

## Candidate 2: feature 2258

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.907`
- validation effect: `+0.876`
- test effect: `+0.688`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.659`

### Top natural activations

1. `act=1.5835` `token='▁saison'`  
   Les saisons changent progressivement dans les zones tempérées.

2. `act=1.5446` `token='▁milieu'`  
   La réforme de la justice fait débat dans les milieux politiques et juridiques.

3. `act=1.5303` `token='▁correo'`  
   Al revisar los correos por la mañana, se sorprendió al encontrar una invitación inesperada a un evento privado en el centro de la ciudad.

4. `act=1.5173` `token='▁vínculo'`  
   Los vínculos familiares en este caso se forman mediante una combinación de parentesco por matrimonio y linaje directo, lo que refleja una estructura social compleja pero bien integrada dentro del sistema de relaciones ampliado.

5. `act=1.4984` `token='▁parcela'`  
   Las parcelas afectadas por la sequía se encuentran actualmente cubiertas de maleza y son consideradas inadecuadas para el cultivo.

6. `act=1.4782` `token='▁milieu'`  
   La sœur du maire de la ville a été nommée présidente du conseil d'administration de l’hôpital universitaire, une décision qui a suscité quelques commentaires dans les milieux politiques locaux.

7. `act=1.4471` `token='▁conflicto'`  
   Los conflictos laborales reflejan tensiones estructurales en la organización del trabajo.

8. `act=1.4471` `token='▁conflicto'`  
   Los conflictos en el trabajo pueden surgir cuando las expectativas de un equipo no coinciden con las normas organizacionales.

## Candidate 3: feature 8911

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.834`
- validation effect: `+0.791`
- test effect: `+0.656`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.590`

### Top natural activations

1. `act=1.3991` `token='s'`  
   Si las condiciones climáticas extremas persistieran por décadas sin solución aparente, probablemente se verían afectadas gravemente las cadenas alimentarias marinas en el Ártico y en otras regiones polares.

2. `act=1.3716` `token='s'`  
   La coopération entre les pays européens a permis d'accélérer le développement des réseaux ferroviaires transfrontaliers, ce qui facilite aujourd'hui les déplacements des citoyens et améliore l'efficacité des chaînes logistiques dans toute la région.

3. `act=1.3385` `token='s'`  
   C’est exactement ce point sur lequel l’équipe de recherche a mis l’accent lors de la présentation de leur découverte, car il change complètement notre compréhension du fonctionnement des circuits quantiques.

4. `act=1.3236` `token='s'`  
   En la biblioteca pública de Madrid, las mesas altas y anchas son ideales tanto para los estudiantes universitarios como para las tareas escolares de los niños.

5. `act=1.3151` `token='s'`  
   La petite bibliothèque de ma fille est pleine de vieux livres d’histoire et de magnifiques bandes dessinées colorées.

6. `act=1.3122` `token='s'`  
   Après le dîner, on a regardé un film en famille, puis on s'est mis à lire des bandes dessinées tranquillement sur le canapé.

7. `act=1.3021` `token='s'`  
   Durante la inspección del almacén, se observó que las cajas se movían solas, pero nadie vio a los trabajadores realizar el movimiento.

8. `act=1.2963` `token='s'`  
   C’est là que l’on s’aperçoit à quel point les réseaux neuronaux artificiels, malgré leurs nombreuses couches de traitement, sont encore loin d’égaler la flexibilité et la plasticité des circuits cérébraux humains dans leur adaptation aux environnements changeants.

## Candidate 4: feature 13837

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.974`
- validation effect: `+0.989`
- test effect: `+0.705`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.166`

### Top natural activations

1. `act=1.5980` `token='▁tareas'`  
   Se había decidido que las tareas críticas del proyecto serían supervisadas directamente por el comité ejecutivo para garantizar una implementación segura y coordinada.

2. `act=1.5877` `token='▁tareas'`  
   Aunque las tareas se reparten equitativamente, muchas veces terminan cayéndome a mí sin que nadie lo discuta.

3. `act=1.5418` `token='▁tareas'`  
   Se notificó al equipo que las tareas debían entregarse antes del cierre de la jornada laboral.

4. `act=1.5402` `token='▁tareas'`  
   El supervisor asignó las tareas al nuevo empleado antes de que comenzara el turno.

5. `act=1.5386` `token='▁tareas'`  
   Las tareas se resolvieron solas al final del día.

6. `act=1.5386` `token='▁tareas'`  
   Las tareas se completaron sin recibir la aprobación previa del equipo de gestión.

7. `act=1.5386` `token='▁tareas'`  
   Las tareas deben ser revisadas cuidadosamente antes de la entrega.

8. `act=1.5386` `token='▁tareas'`  
   Las tareas fueron entregadas sin que se mencionara el nombre del estudiante.

## Candidate 5: feature 8113

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.885`
- validation effect: `+0.884`
- test effect: `+0.702`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.162`

### Top natural activations

1. `act=0.9208` `token='▁एक'`  
   बस के अंदर मेरी बेटी, उसका दोस्त और एक पुलिसवाला खड़े थे, सभी ने एक-एक करके अपना घर छोड़ा था और गांव के बाजार जा रहे थे।

2. `act=0.9009` `token='▁gathered'`  
   All the children, along with their parents, gathered in the backyard to celebrate the grandmother’s birthday, each carrying a gift they had chosen together.

3. `act=0.8934` `token='▁एक'`  
   पुलिस ने कहा कि लगभग पचास लोग एक संगठित ढंग से जलीकट्टई शो के लिए तैयारियों में लगे हुए हैं।

4. `act=0.8811` `token='▁girdi'`  
   Dünkü toplantıda karar verildikten sonra herkes içeri girdi ama ben hâlâ dışarıdaydım.

5. `act=0.8720` `token='▁présent'`  
   La pièce a eu lieu hier soir et tout le monde était présent à l’heure prévue.

6. `act=0.8692` `token='▁gathered'`  
   All the kids in the camp gathered around the bonfire to share stories.

7. `act=0.8640` `token='▁ama'`  
   Birlikte çalışan onlarca kişi vardı ama kimse ona yardım etmedi.

8. `act=0.8623` `token='▁حضر'`  
   أعجب الطلاب الثلاثة الذين حضروا الحصة الخاصة بالرماية النتائج التي حققها الفريق الرياضي في المسابقة الأخيرة.

---

# Variable 12: optionality_vs_obligatoriness_of_marking

- Original SAE evidence tier: **B2**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.724**

## Candidate 1: feature 9607

- selection: `original_trainval_selected`
- train effect: `+0.404`
- validation effect: `+0.519`
- test effect: `+0.538`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.526`

### Top natural activations

1. `act=1.0058` `token='時'`  
   昨日の会見で、官僚が緊急対応を表明した時にもかかわらず国民に説明を怠ったことに対して、多くの市民はなぜその責任が問われていないのか不満を抱いている。

2. `act=1.0045` `token='時'`  
   サッカーの試合で、相手チームが予想外にリードしてしまった時、観客は驚きの表情を浮かべていました。

3. `act=0.9640` `token='時'`  
   飛行機で到着した時、こんなに暑いとは思わなかった。

4. `act=0.9602` `token='時'`  
   まさかあんなに遠くまで足を運ぶことになるなんて、新幹線で迷子になった時に気付いた時、本当にびっくりしてしまったよ。

5. `act=0.9522` `token='時'`  
   試合開始時、彼はゴール前のパスを受ける位置にいたが、終盤には攻撃の起点として後ろからプレッシャーをかけ始めた。

6. `act=0.9507` `token='時'`  
   彼が到着した時、すでに夜遅くだった。

7. `act=0.9373` `token='時'`  
   会議の開始時刻が午前10時に決まったため、このままでは新幹線で到着する予定の国際的なゲストに少し早い時間に駅から送迎を依頼することになり、事務局長はそれについて一足早く連絡するようにと秘書に言い渡しました。

8. `act=0.9369` `token='時'`  
   今天早上我起床時，發現陽光已經灑進客廳，而隔壁鄰居的貓正從圍牆上跳下來，大概是聽到我的腳步聲才躲進了後院。

## Candidate 2: feature 7165

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.403`
- validation effect: `-0.277`
- test effect: `-0.038`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.430`

### Top natural activations

1. `act=0.6014` `token='住'`  
   その道を歩きながら観光客は写真を撮り、地元の住民は買い物をしていた。

2. `act=0.5954` `token='住'`  
   この事件について、地元の住民は深い懸念を示しています。

3. `act=0.5941` `token='住'`  
   電車で会社に向かっている途中でかつて住んでいた街の隣町を通ったとき、ふと通り過ぎた駅の名前が耳に届いて、懐かしさに胸がキュッてなって、昨日までそこ暮らしだったような気持ちになったんだよね。

4. `act=0.5823` `token='乘'`  
   由於飛機班號為CA1258的航班因天氣原因延誤，乘客們在航站樓的電子屏上看到顯示「#取消動態更新_CA1258」的提示時，紛紛前往服務櫃檯詢問改簽事宜。

5. `act=0.5708` `token='m'`  
   Kokeellisessa tutkimuksessa käytettiin monimutkaista laitetta, joka mittasi yksittäisten elektronien kulkua eri magneettikenttien läpi hiukkaskiihdyttimen laskentamallissa.

6. `act=0.5681` `token='住'`  
   お寺の境内を散歩していると、由緒ある茶室で有名な住職様が来られまして、私たちに丁寧にお話しくださり、日本の伝統文化の大切さについて心から学ばせていただきました。

7. `act=0.5614` `token='m'`  
   Tieteellisessä tutkimuksessa voidaan käyttää monenlaisia matemaattisia menetelmiä tilastollisen datan analysoimiseen.

8. `act=0.5614` `token='m'`  
   Tieteellisessä tutkimuksessa käytetyt monimutkaiset sanoja muodostavat helposti ymmärrettävän kuvauksen ilman tarvetta useille erillisille sanoille.

## Candidate 3: feature 13817

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.418`
- validation effect: `-0.940`
- test effect: `-0.199`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.245`

### Top natural activations

1. `act=0.7312` `token='那'`  
   这幅画描绘了当地的日常生活，而那幅画则展现了遥远城市的情景。

2. `act=0.7231` `token='那'`  
   会议桌上这份文件非常重要，我们必须在今天下午之前完成它，而那份放在你桌上的则是下一阶段项目的初步方案。

3. `act=0.6842` `token='那'`  
   比賽就在那裡進行，我們在這邊看。

4. `act=0.6737` `token='那'`  
   这本相册记录了我们去年夏天在老家的全家合影，而那边墙上挂着的是祖父年轻时与祖母结婚的照片。

5. `act=0.6661` `token='那'`  
   这间咖啡馆的座位靠近窗户，而那边的长椅上已经坐满了人。

6. `act=0.6636` `token='那'`  
   这里夏天的蝉鸣总是比别处更响亮，仿佛整个山谷都在回应它们的声音，而那边的小溪旁，人们则喜欢在树荫下闲聊，享受清凉的风和自然的宁静。

7. `act=0.6607` `token='那'`  
   我发现，尽管人工智能在科学研究中展现出惊人的效率和准确性，但它依然无法替代人类科学家那种基于直觉和经验的独特洞察力。

8. `act=0.6584` `token='那'`  
   这台机器的显示屏上出现了几个奇怪的数据点，而那边的控制面板却没有任何反应。

## Candidate 4: feature 47

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.412`
- validation effect: `+0.808`
- test effect: `+0.180`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.993`

### Top natural activations

1. `act=0.8116` `token='渡'`  
   博物館の見学を終えられた後で、先生のご希望に応じてガイドが用意した特別なアート作品解説書をお渡ししました。

2. `act=0.7259` `token='播'`  
   我昨天在机场候机大厅等了将近两个小时，本来应该十点起飞的航班因为前一晚有乘客突发健康问题导致延误，现在广播刚通知要等到中午十二点半，坐在旁边的外国老太太一直咳嗽还戴了口罩，我觉得她可能是有点感冒或者呼吸道不适。

3. `act=0.6931` `token='渡'`  
   課長に資料をお渡し申し上げました。

4. `act=0.6893` `token='ذ'`  
   جاء الضيف من دون حذاء وطلب كوب من الشاي البارد.

5. `act=0.6835` `token='渡'`  
   お父様には書類をお渡ししました。

6. `act=0.6725` `token='ذ'`  
   لقد ذهب الأخ الأكبر إلى الصالة الرياضية بعد أن اشترى حذاءً جديدًا من العلامة التجارية المفضلة لديه لكي يلعب كرة السلة مع الأصدقاء كل مساء في فترة ما بعد الظهر.

7. `act=0.6691` `token='覧'`  
   お母様のご希望でしたら、その芸術展観覧には同行させていただきます。

8. `act=0.6676` `token='ذ'`  
   بينما كانت الأم تنتعل حذاءها وتستعد للمغادرة المنزل لحضور اجتماع مهم، أخذت ابنتها الصغيرة قطعة قماش بلون الأرجواني وبدأت بصنع لعبة عيد الميلاد بمساعدة الجار المسن الذي يحب الأطفال ويتمتع بإبداع غير منتهي في صنع الورود الورقية والأشجار الزخرفية.

## Candidate 5: feature 10454

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.424`
- validation effect: `-0.965`
- test effect: `-0.181`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.966`

### Top natural activations

1. `act=1.4015` `token='▁इस'`  
   विज्ञान और कला के संगम पर आधारित इस चित्रकला प्रदर्शनी में, नए उभरते कलाकारों ने अपनी अद्वितीय शैलियों के माध्यम से दर्शकों को अपनी ओर खींच लिया।

2. `act=1.3800` `token='▁इस'`  
   मेरी बहन का इस नए प्रौद्योगिकी अविष्कार में बड़ा योगदान है।

3. `act=1.3569` `token='▁इस'`  
   राज्य के मुख्यमंत्री ने आज एक बड़े आयोजन में अपने राज्य के विकास के लिए नए नीति निर्णयों की घोषणा करते हुए कहा कि आज के इस नए दौर में सभी लोगों के साथ न्याय और समानता की भावना के साथ चलना ही आवश्यक है।

4. `act=1.3261` `token='▁इस'`  
   महोदय शिक्षक जी, क्या आप हमें इस अनुच्छेद पर एक लेख लिखने में सहायता कर सकते हैं?

5. `act=1.3190` `token='▁इस'`  
   महाकाव्यों और नाटकों के अलावा, इस क्षेत्र में छोटे कहानी संग्रह भी बहुत लोकप्रिय हैं, जो प्राचीन दंतकथाओं और लोक नृत्यों की ओर इशारा करते हैं।

6. `act=1.3143` `token='▁इस'`  
   हम लोग सभी कलाकारों के साथ मिलकर इस क्लब में संगीत से अपना मज़ा ले रहे थे।

7. `act=1.3073` `token='▁इस'`  
   मुख्य सचिव के आदेश पर ही इस मामले में त्वरित कार्रवाई की गई।

8. `act=1.3069` `token='▁इस'`  
   कृत्रिम बुद्धिमता के इस प्रणाली में जीवित एवं अजीवित वस्तुओं को भेद से पहचानने की क्षमता होगी।

---

# Variable 13: redundancy_cumulative_exponence

- Original SAE evidence tier: **A**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.785**

## Candidate 1: feature 9749

- selection: `original_trainval_selected`
- train effect: `-0.681`
- validation effect: `-0.836`
- test effect: `-0.775`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.890`

### Top natural activations

1. `act=1.5730` `token='▁para'`  
   Aunque le había dicho mil veces que no olvidara el paraguas, cuando llegó la tormenta, lo tuvo que pedir prestado al vecino de al lado.

2. `act=1.5639` `token='▁para'`  
   No me gustó para nada la forma en que te hablaste conmigo.

3. `act=1.5337` `token='▁para'`  
   Aquí tienes el regalo para ti, y allá están los tuyos para los demás.

4. `act=1.5277` `token='▁para'`  
   El profesor les leyó en voz alta el artículo para que todos lo entendieran mejor.

5. `act=1.5150` `token='▁para'`  
   Todavía no nos comimos ninguna de las galletas que nos hizo nuestra abuela para la merienda del fin de semana.

6. `act=1.4969` `token='▁para'`  
   Anoche me dolía la cabeza y tomé paracetamol.

7. `act=1.4958` `token='▁para'`  
   El paisaje pertenece al artista, pero la montaña sigue siendo suya para siempre.

8. `act=1.4953` `token='▁para'`  
   Bueno, como todos sabemos que hoy va a hacer calor, seguramente María se habrá olvidado de traer el paraguas, aunque sea probable que haya pensado en ello antes de salir de casa.

## Candidate 2: feature 11745

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.632`
- validation effect: `+0.697`
- test effect: `+0.471`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.742`

### Top natural activations

1. `act=0.5937` `token='▁деятельность'`  
   Все работники крупного научного центра вчерwu были награждены благодарственными письмами за выдающийся вклад в исследовательскую деятельность и высокий профессиональный уровень выполнения своих обязанностей.

2. `act=0.5732` `token='▁безопасность'`  
   Сотрудники полиции сопровождали задержанного подозреваемого на допрос в специальном транспорте, чтобы предотвратить возможное побег и обеспечить безопасность общества.

3. `act=0.5601` `token='▁безопасности'`  
   Всем сотрудникам отдела перевозок необходимо пройти инструктаж по технике безопасности перед началом работ на складе.

4. `act=0.5596` `token='е'`  
   Сотрудник отдела продаж закончил подготовку нового презентационного слайда и передал его директору на согласование за полчаса до начала встречи с потенциальным клиентом.

5. `act=0.5567` `token='альность'`  
   Картинам этого художника присущи яркие краски и глубокая эмоциональность.

6. `act=0.5531` `token='ляция'`  
   Работая над новым альбомом, коллектив уже третий месяц репетирует те самые песни, что впоследствии будут звучать на фестивале и в прямых трансляциях.

7. `act=0.5511` `token='ацию'`  
   Специалист по IT успешно завершил установку нового программного обеспечения на сервере и передал техническую документацию для проверки отделу качества.

8. `act=0.5487` `token='чность'`  
   Учёные неоднократно проверяли установку на прочность и каждый раз замечали, как тонкая структура данных проявляется в виде линий и кривых на экране, пока конечный результат моделирования не станет достаточно чётким для анализа.

## Candidate 3: feature 4814

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.705`
- validation effect: `+0.928`
- test effect: `+0.455`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.660`

### Top natural activations

1. `act=1.9290` `token='ительным'`  
   Отец сына помогает ему с подготовкой к вступительным экзаменам в университет.

2. `act=1.8042` `token='онного'`  
   Все сотрудники команды приняли участие в подготовке квалификационного этапа чемпионата.

3. `act=1.7311` `token='ным'`  
   Рабочие места должны соответствовать санитарным нормам.

4. `act=1.7242` `token='ым'`  
   Генеральный прокурор страны заявил, что в ходе расследования были выявлены серьёзные нарушения со стороны чиновников, включая присвоение государственных средств и злоупотребление служебным положением.

5. `act=1.6881` `token='ным'`  
   Сотрудники предприятия по производству продуктов питания регулярно проверяют условия хранения и температурный режим, чтобы убедиться, что продукты соответствуют санитарным нормам и безопасны для потребителей.

6. `act=1.6597` `token='ым'`  
   Вчера в художественной галерее прошёл мастер-класс по акробатике, на котором учили базовым элементам современного жанра.

7. `act=1.6527` `token='ным'`  
   Правительство страны объявило о планах предоставить местным предприятиям дополнительные субсидии и расширить доступ к кредитным линиям в рамках усилий по поддержке экономики в условиях роста инфляции.

8. `act=1.6342` `token='ным'`  
   Борт инженер проверяет показания систем управления полётом и подтверждает их соответствие нормативным требованиям перед началом предполётной подготовки.

## Candidate 4: feature 790

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.667`
- validation effect: `-0.576`
- test effect: `-0.635`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.254`

### Top natural activations

1. `act=1.4279` `token='.'`  
   Для повышения иммунитета врачи рекомендуют регулярно употреблять витамин С.

2. `act=1.4275` `token='.'`  
   У пациента часто болит голова.

3. `act=1.4198` `token='.'`  
   Во многих аптеках Европы не все лекарства продаются без рецепта врача.

4. `act=1.4150` `token='.'`  
   У пожилого человека часто возникают проблемы с восстановлением после операции.

5. `act=1.4147` `token='.'`  
   В республике каждый день в школах проходят проверки на содержание наркотиков.

6. `act=1.4120` `token='.'`  
   Пациент передал лекарство врачу после консультации в поликлинике.

7. `act=1.4055` `token='.'`  
   Родительский контроль важен для развития ребенка.

8. `act=1.4002` `token='.'`  
   В аптеке можно найти лекарства от простуды в пачках по тридцать таблеток.

## Candidate 5: feature 10612

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.768`
- validation effect: `+0.731`
- test effect: `+0.174`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.254`

### Top natural activations

1. `act=1.3944` `token='▁намерени'`  
   Ни один из друзей не догадался о её намерении уйти.

2. `act=1.3895` `token='▁композици'`  
   Художник, работая над новым портретом, ввёл в композицию нежный намёк на пейзаж, чтобы придать лицу дополнительную глубину и эмоциональное напряжение.

3. `act=1.3868` `token='▁расписани'`  
   Пациенту не разрешалось покидать палату без сопровождения медсестры, и все предписанные лекарства он принимал строго по расписанию, несмотря на то что некоторые из них вызывали неприятные побочные эффекты.

4. `act=1.3607` `token='▁одобрени'`  
   Когда мы обсуждали изменения в расписании встречи, предложение сотрудника было принято без споров, и руководитель высказал своё одобрение в ходе общего собрания.

5. `act=1.3584` `token='гласи'`  
   Соперники по команде часто ссорились из-за разногласий в тактике, но каждый вечер они неизменно восстанавливали доброжелательную атмосферу за чашкой чая и обсуждением предстоящего матча.

6. `act=1.3573` `token='liikentee'`  
   Lentokone saapui viimeiseksi pakettiliikenteellä.

7. `act=1.3496` `token='▁коррупци'`  
   Когда правит коррупция, страна теряет доверие граждан.

8. `act=1.3481` `token='▁коррупци'`  
   Сотрудники пострадавших от коррупции общественных организаций обратились к суду с коллективным заявлением.

---

# Variable 14: definiteness_and_specificity

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.992**

## Candidate 1: feature 13819

- selection: `original_trainval_selected`
- train effect: `-0.508`
- validation effect: `-0.483`
- test effect: `-0.528`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.359`

### Top natural activations

1. `act=1.1553` `token='▁часто'`  
   Инженеры и учёные часто взаимодействуют между собой во время разработки сложных технологий для решения общих проблем и достижения важных целей в области науки и техники.

2. `act=1.1209` `token='▁часто'`  
   Учёные часто проводят эксперименты, чтобы проверить гипотезы и получить новые данные.

3. `act=1.1209` `token='▁часто'`  
   Учёные часто изучают поведение атомов в кристаллической решётке при различных температурах.

4. `act=1.1209` `token='▁часто'`  
   Учёные часто наблюдают за поведением этих животных.

5. `act=1.1209` `token='▁часто'`  
   Учёные часто изучают поведение звёзд, чтобы понять устройство Вселенной.

6. `act=1.1197` `token='▁часто'`  
   Троллейбусы часто становятся удобным способом добраться до центра города.

7. `act=1.1181` `token='▁часто'`  
   Музыка старины часто звучит тише, чем современные композиции.

8. `act=1.1175` `token='▁часто'`  
   Научные исследования часто проводятся без указания конкретного исследователя.

## Candidate 2: feature 3973

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.548`
- validation effect: `-0.627`
- test effect: `-0.505`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.271`

### Top natural activations

1. `act=0.6792` `token='ない'`  
   体調がよくないなら、無理に動こうとしないで休むほうがいい。

2. `act=0.6792` `token='ない'`  
   体調がよくないなんて、ほんとびっくりしたよ。

3. `act=0.6792` `token='ない'`  
   体調がよくないなんて、びっくりしたよ。

4. `act=0.6792` `token='ない'`  
   体調がよくないときは、自宅で休むのが一番ですよ。

5. `act=0.6751` `token='ない'`  
   この薬、体がよくないときに飲むと効くよ。

6. `act=0.6732` `token='▁zor'`  
   Okulda öğrendiklerimi işte kullanabilmek her zaman zor oldu.

7. `act=0.6610` `token='ない'`  
   なんてことない授業が、実際に始まってみたらものすごく面白くて驚きました！

8. `act=0.6610` `token='ない'`  
   なんてことないテスト問題が、実はとても難しくて、みんな驚いていました。

## Candidate 3: feature 15695

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.473`
- validation effect: `-0.387`
- test effect: `-0.476`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.114`

### Top natural activations

1. `act=1.3013` `token='▁falta'`  
   Es posible que la falta de síntomas indique una recuperación avanzada del paciente.

2. `act=1.2638` `token='▁falta'`  
   A pesar de que el gobierno anunció un nuevo plan económico para estabilizar la moneda nacional, los analistas advierten que sin medidas contundentes contra la corrupción, cualquier política monetaria se verá en vano socavada por la falta de confianza del sector privado.

3. `act=1.2628` `token='▁falta'`  
   Allí, donde el sol aún tardaba en calentar el asfalto, el autobús llegó con retraso, lo que provocó que mucha gente se quedara sin lugar y tuviera que esperar otro mientras protestaban por la falta de puntualidad.

4. `act=1.2611` `token='▁falta'`  
   Por más que los investigadores dedicaran esfuerzos considerables al diseño del experimento, resultó evidente que la falta de representación adecuada en la muestra afectó negativamente la validez de los resultados obtenidos.

5. `act=1.2602` `token='▁falta'`  
   En los países pobres, la falta de agua potable afecta a millones de personas cada día.

6. `act=1.2597` `token='▁falta'`  
   El alcalde visitó la escuela primaria para escuchar las preocupaciones de los docentes y padres, quienes manifestaron su insatisfacción con la falta de recursos y el retraso en los proyectos anunciados por el gobierno municipal.

7. `act=1.2562` `token='▁falta'`  
   El vecino y sus hijos recorren el barrio protestando por la falta de alumbrado público.

8. `act=1.2532` `token='▁falta'`  
   Aunque los estudiantes manifestaron su preocupación por la falta de recursos en la escuela, el director les aseguró que estaba trabajando activamente para mejorar las condiciones y solicitar apoyo a las autoridades educativas locales.

## Candidate 4: feature 12995

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.474`
- validation effect: `-0.437`
- test effect: `-0.421`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.072`

### Top natural activations

1. `act=1.0017` `token='一'`  
   山を見上げて、私はただ一言、「すばらしいですね」と呟きました。

2. `act=0.9991` `token='一'`  
   試合終了間際、守備中の選手がボールをしっかりと捕球するも、走者があと一歩のところで踏み切ったことによって、逆転のホームランが生まれた。

3. `act=0.9571` `token='一'`  
   この実験器具は専門の棚に置かなければならないが、今のところ一時的に机の上にでも構わない。

4. `act=0.9475` `token='一'`  
   芸術作品が持つ意味は、観る人の解釈によって異なるため、一義的には決定されない。

5. `act=0.9449` `token='一'`  
   紅茶の香りが部屋中に広がり、小さな窓辺で読書をしていた彼女は、夕暮れ時の静けさと温かさを感じながら、一層のくつろぎの中に包まれていった。

6. `act=0.9439` `token='一'`  
   お母様がご旅行中に、私は一歩一歩丁寧にお手伝いさせていただき、空港までの送迎を務めることを心より嬉しく思っております。

7. `act=0.9375` `token='一'`  
   古い街を歩きながら、私は通りに面した小さな茶屋で一休みし、そこで見た芸術作品と地元の文化について考えていた。

8. `act=0.9332` `token='一'`  
   あそこに見えるカフェで一息つこうか、この辺りは歩き疲れそうだよ。

## Candidate 5: feature 14259

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.509`
- validation effect: `-0.436`
- test effect: `-0.458`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.036`

### Top natural activations

1. `act=1.0257` `token='▁küçük'`  
   Güvenli bir şekilde yürütülmektedir bu operasyon, ilk başta sadece küçük bir ekip tarafından planlanmış olsa da zamanla daha geniş kapsamlı hale geldi.

2. `act=0.9941` `token='▁hanya'`  
   Kami sedang merencanakan acara kecil hanya untuk kami dan keluarga dekat minggu ini.

3. `act=0.9796` `token='▁छोट'`  
   मेरे पिताजी ने मुझे सब से पहले बताया था कि किसी चीज़ को ख़रीदने के बाद उसकी ध्यान से देखभाल करना चाहिए, चाहे वो एक छोटा सा बर्तन हो या फिर

4. `act=0.9299` `token='▁kleine'`  
   Die Ministerin betonte ausdrücklich, dass die neue Regelung vor allem kleine Betriebe betrifft.

5. `act=0.9204` `token='▁just'`  
   My teacher said that the students who ask questions often seem to learn the most, even if they're just repeating what someone else has said.

6. `act=0.9154` `token='ा'`  
   दफ्तर में काम करने वाले छह नए टीम मेंबर पिछले सप्ताह शामिल हुए और उनका स्वागत करते हुए सभी कर्मचारियों ने एक छोटा सा धूमधाम से पार्टी आयोजित की

7. `act=0.9144` `token='ste'`  
   Wer die Tagesabläufe in der stillen Eleganz eines alten Opernhauses verfolgt, der erkennt, dass gerade die kleinste Bewegung des Vorhangs eine Welt voller Stille und Sehnsucht erzählen kann.

8. `act=0.9137` `token='い'`  
   展覧会のオープニングに合わせて、アーティストは自身の制作過程を映した短いドキュメンタリーを上映した。

---

# Variable 15: number_marking

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.488**

## Candidate 1: feature 8113

- selection: `original_trainval_selected`
- train effect: `+0.762`
- validation effect: `+0.204`
- test effect: `-0.045`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.861`

### Top natural activations

1. `act=0.9208` `token='▁एक'`  
   बस के अंदर मेरी बेटी, उसका दोस्त और एक पुलिसवाला खड़े थे, सभी ने एक-एक करके अपना घर छोड़ा था और गांव के बाजार जा रहे थे।

2. `act=0.9009` `token='▁gathered'`  
   All the children, along with their parents, gathered in the backyard to celebrate the grandmother’s birthday, each carrying a gift they had chosen together.

3. `act=0.8934` `token='▁एक'`  
   पुलिस ने कहा कि लगभग पचास लोग एक संगठित ढंग से जलीकट्टई शो के लिए तैयारियों में लगे हुए हैं।

4. `act=0.8811` `token='▁girdi'`  
   Dünkü toplantıda karar verildikten sonra herkes içeri girdi ama ben hâlâ dışarıdaydım.

5. `act=0.8720` `token='▁présent'`  
   La pièce a eu lieu hier soir et tout le monde était présent à l’heure prévue.

6. `act=0.8692` `token='▁gathered'`  
   All the kids in the camp gathered around the bonfire to share stories.

7. `act=0.8640` `token='▁ama'`  
   Birlikte çalışan onlarca kişi vardı ama kimse ona yardım etmedi.

8. `act=0.8623` `token='▁حضر'`  
   أعجب الطلاب الثلاثة الذين حضروا الحصة الخاصة بالرماية النتائج التي حققها الفريق الرياضي في المسابقة الأخيرة.

## Candidate 2: feature 13837

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.836`
- validation effect: `+0.099`
- test effect: `+0.646`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.858`

### Top natural activations

1. `act=1.5980` `token='▁tareas'`  
   Se había decidido que las tareas críticas del proyecto serían supervisadas directamente por el comité ejecutivo para garantizar una implementación segura y coordinada.

2. `act=1.5877` `token='▁tareas'`  
   Aunque las tareas se reparten equitativamente, muchas veces terminan cayéndome a mí sin que nadie lo discuta.

3. `act=1.5418` `token='▁tareas'`  
   Se notificó al equipo que las tareas debían entregarse antes del cierre de la jornada laboral.

4. `act=1.5402` `token='▁tareas'`  
   El supervisor asignó las tareas al nuevo empleado antes de que comenzara el turno.

5. `act=1.5386` `token='▁tareas'`  
   Las tareas se resolvieron solas al final del día.

6. `act=1.5386` `token='▁tareas'`  
   Las tareas se completaron sin recibir la aprobación previa del equipo de gestión.

7. `act=1.5386` `token='▁tareas'`  
   Las tareas deben ser revisadas cuidadosamente antes de la entrega.

8. `act=1.5386` `token='▁tareas'`  
   Las tareas fueron entregadas sin que se mencionara el nombre del estudiante.

## Candidate 3: feature 8685

- selection: `train_fwer_only`
- train effect: `+0.783`
- validation effect: `-0.560`
- test effect: `-0.393`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.455`

### Top natural activations

1. `act=0.9442` `token='s'`  
   Bare noun phrase example: Chickens roam near the research station. Determined noun phrase example: The chickens roam near the research station.

2. `act=0.9159` `token='s'`  
   I think he might have meant that painting by the window, the one with the sunflowers, though I'm not entirely sure since he usually refers to it as "the cheerful one."

3. `act=0.9067` `token='s'`  
   As I wandered through the crowded marketplace, a local vendor called out, “These spices are fresh today,” which he confirmed later by adding that they had just arrived from the nearby hills.

4. `act=0.9042` `token='ों'`  
   मैंने अपनी बालकनी में एक छोटा फूलों का बाग लगाया है, जिसमें चमेली, गुलाब और जैतून के पौधे शामिल हैं, जो न केवल खूबसूरत दिखते हैं बल्कि मक्खियों को भी आकर्षित करते हैं।

5. `act=0.9018` `token='s'`  
   He gave her the keys to his car and his apartment, just in case she needed anything at all.

6. `act=0.8933` `token='s'`  
   Yesterday, she painted the sunset just before it vanished behind the hills.

7. `act=0.8635` `token='s'`  
   She handed me the keys to her car and told me where to find the spare tire.

8. `act=0.8635` `token='s'`  
   She handed me the keys without a word.

## Candidate 4: feature 8793

- selection: `train_fwer_only`
- train effect: `+0.753`
- validation effect: `-0.473`
- test effect: `+0.230`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `True`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.057`

### Top natural activations

1. `act=3.1076` `token='lim'`  
   Hiçbir zaman cesaretin kaybetmeyelim.

2. `act=3.1064` `token='n'`  
   Köpekçi kuşlar yuvalarını ağaçtaki dağlıktan sessizce temizlediler ama çocukların sesleri onları tekrar gizlenmeye zorladı.

3. `act=3.0809` `token='▁aus'`  
   Ein gesunder Lebensstil schließt aus, den Stress nicht zu ignorieren und sich regelmäßig körperlich zu betätigen.

4. `act=3.0805` `token='ले'`  
   मैंने रात भर चावल उबाले रखे थे, लेकिन फिर उन्हें ठंडा हो जाने के बजाय उन्हें एक बार फिर उबाल लिया ताकि पूरा परिवार गर्म और स्वादिष्ट भोजन कर सके।

5. `act=3.0803` `token='▁sein'`  
   Ich musste gestern Abend mit dem Zug fahren, weil ich am Morgen um halb sieben in der Firma sein sollte, und da ich ohnehin schon im Büro war, blieb mir nichts anderes übrig, als den Zug zu nehmen, auch wenn es der letzte war.

6. `act=3.0777` `token='a'`  
   Otobüste on yolcu bizimle birlikte duraklara uğramadan yola devam etti.

7. `act=3.0717` `token='▁sein'`  
   Ich glaube, dass er den Kuchen nicht mag, weil er ihn meist stehen lässt, aber sicher kann ich mir da nicht sein.

8. `act=3.0671` `token='으로'`  
   할머니는 손녀를 부엌으로 불러들여 직접 반죽을 만드는 법을 가르쳐 주셨고, 그 덕분에 집안의 전통 떡 메뉴가 젊은 세대에게 자연스럽게 물려받아졌습니다.

## Candidate 5: feature 995

- selection: `train_fwer_only`
- train effect: `+0.842`
- validation effect: `-0.211`
- test effect: `-0.092`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.055`

### Top natural activations

1. `act=1.5802` `token='ों'`  
   सरकार द्वारा प्रमुख शहरों में एकीकृत यातायात प्रणाली के विकास की अनुमति देकर सभी प्रकार के परिवहन साधनों के बीच संयुक्त संचालन को बढ़ावा देने का

2. `act=1.5725` `token='ల'`  
   మా సంస్థలో కలిసి పని చేయడం ద్వారా మేము చాలా విజయాలను సాధించగలమని, గత నెలలో పూర్తి అయిన ప్రాజెక్టుల ద్వారా నిరూపించుకున్నాము.

3. `act=1.5412` `token='ों'`  
   भारतीय चित्रकला के अत्यंत समृद्ध इतिहास में बनारसी पट चित्र, मन्दिरों की अनूठी वास्तुकला और रंगमंच पर नाटकों की नाट्यात्मक प्रस्तुति भी एक विशिष्ट विरासत है।

4. `act=1.5400` `token='ల'`  
   మేము ఈ పరిశోధనలో భాగం కాకుండా సమస్యల పరిష్కారాలను అభివృద్ధి చేసాము.

5. `act=1.5361` `token='وں'`  
   وہ بارش کو اپنے ہاتھوں میں لے کر گھروں تک پانی پہنچا رہا تھا۔

6. `act=1.5186` `token='وں'`  
   عید کے موقع پر امیروں کا گراؤنڈ تقریب کے لیے بھر گیا تھا جہاں والدین اپنے بچوں کو فٹبال کھیلنے کے لیے مشغول دیکھتے ہوئے سکون محسوس کر رہے تھے۔

7. `act=1.4953` `token='jen'`  
   Kävelin autojen välistä käytävällä.

8. `act=1.4753` `token='ों'`  
   महाकाव्यों के जनक मुकेश बचपन से ही प्रकृति की सुंदरता और मनुष्यों के सामान्य चिंतन के बारे में लिखने के शौक में डूबे रहते थे।

---

# Variable 16: gender_noun_class

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 5205

- selection: `original_trainval_selected`
- train effect: `+0.897`
- validation effect: `+0.908`
- test effect: `+0.909`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.578`

### Top natural activations

1. `act=1.3319` `token='ی'`  
   میں نے اپنی بچی کو دفتر سے گھر آتے ہی درسی پڑھ لینا شروع کردیا۔

2. `act=1.3103` `token='ی'`  
   اُس نے اپنی بچی کو بستر پر لیٹائے ہوئے دیکھا جب وہ میز پر ایک خاص سانچے کے ساتھ گرم چائے کا کپ رکھتی اور ان دونوں کے درمیان دل کی باتیں چلتی رہیں۔

3. `act=1.2962` `token='ة'`  
   في المكتب الجديد، بدأ الموظفون العمل بجدّ مع المديرة الجديدة التي تظهر حماسها في كل تصريح.

4. `act=1.2931` `token='ة'`  
   تدرّس الأستاذة الرياضيات.

5. `act=1.2910` `token='ة'`  
   بينما كان الموظف يراجع التقرير النهائي الذي أعدّه فريقه، تلّقى اتصالاً من المديرة التنفيذية طلبت فيه من المرأة أن تستعد للقاء غير مخطط له مع شريك تجاري مهم، مما اضطرها إلى تأجيل عطلتها الأسبوعية المقررة في نفس اليوم.

6. `act=1.2880` `token='ة'`  
   إن الطالب المحترم قد أبدى اهتمامه الجاد بموضوع البحث الذي تناقشه الأستاذة مع فصلها الثاني.

7. `act=1.2818` `token='ی'`  
   چچا نے بچی کو اپنی گود میں بٹھالے۔

8. `act=1.2809` `token='ة'`  
   مَرَّ الطالبُ المتفوقُ بجانبِ مكتبةِ المدرسةِ ليتلقى علويًا نصيحةً من الأستاذةِ التي تشاركُهُ حبَّ القراءةِ.

## Candidate 2: feature 12965

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.949`
- validation effect: `-0.944`
- test effect: `-0.909`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.041`

### Top natural activations

1. `act=0.4342` `token='▁عل'`  
   علّم الطالب.

2. `act=0.4241` `token='▁الطائ'`  
   الطائرة أقلعت من المطار بسلاسة دون أي تأخير ملحوظ.

3. `act=0.4218` `token='▁هر'`  
   هرّب الكلب الكرة.

4. `act=0.4218` `token='▁هر'`  
   هربت الصغيرة من البيت لانها كانت متعبة.

5. `act=0.4186` `token='▁الأم'`  
   الأمّ جاهزة للطعام.

6. `act=0.4178` `token='▁Hinter'`  
   Hinter der Tür auf dem Flur stand die frischgebackene Pfanne mit den Spaghetti, den Rosinen und dem Parmesan, die ich vorhin für das Abendessen vorbereitet hatte.

7. `act=0.4148` `token='▁تأ'`  
   تأكل الأوراق الخضراء الشمس.

8. `act=0.4148` `token='▁تأ'`  
   تأكل الأم.

## Candidate 3: feature 1671

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.950`
- validation effect: `-0.957`
- test effect: `-0.925`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.022`

### Top natural activations

1. `act=0.8274` `token='▁नदी'`  
   बच्चे नदी के किनारे एक पत्थर को हिलाते हुए उसमें से छिपे हुए मछलियों को देखने लगे।

2. `act=0.8111` `token='▁बेट'`  
   बेटे की शादी के बारे में उसकी माँ और पिता की राय अलग-अलग है।

3. `act=0.8111` `token='▁बेट'`  
   बेटा, अपने चाचा को समय पर मिल जाओ, वह तुम्हारे पिताजी के साथ अच्छे संबंध रखते हैं और उनके आशीर्वाद से काम बहुत आसान हो जाएगा।

4. `act=0.8064` `token='▁कार्यकर्ता'`  
   कार्यकर्ता ने अपने बॉस को प्रबंधन द्वारा जारी एक महत्वपूर्ण पत्र दिया।

5. `act=0.8064` `token='▁कार्यकर्ता'`  
   कार्यकर्ता ने समिति की बैठक में नए प्रस्ताव का संशोधन कर दिया।

6. `act=0.8064` `token='▁कार्यकर्ता'`  
   कार्यकर्ता ने प्रबंधक से कहा कि रिपोर्ट अभी तक अपडेट नहीं हुई है।

7. `act=0.8064` `token='▁कार्यकर्ता'`  
   कार्यकर्ता को अपनी नौकरी में एक नई समस्या से निपटना पड़ा।

8. `act=0.8064` `token='▁कार्यकर्ता'`  
   कार्यकर्ता को अधिकारी ने बताया कि परियोजना में समस्या के कारण देरी हुई।

## Candidate 4: feature 3570

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.925`
- validation effect: `-0.915`
- test effect: `-0.806`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.006`

### Top natural activations

1. `act=0.6036` `token='▁30.'`  
   30. yüzyılda Cumhuriyet'in temelleri atılan bu şehir, sanat ve kültüre ev sahipliği yapmaya devam ediyor.

2. `act=0.5878` `token='▁அப்பா'`  
   அப்பா கிரிக்கெட் பந்து வாங்கிய பிறகு, நானும் உங்களும் களத்தில் பயிற்சி செய்து கொள்ளலாம்.

3. `act=0.5878` `token='▁அப்பா'`  
   அப்பா என்னைக் குழந்தைப் பருவம் முதலே வினைத்தொழிலில் ஈடுபடுத்தியிருந்தார்.

4. `act=0.5878` `token='▁அப்பா'`  
   அப்பா மற்றும் நான் இன்று காலையில் ஒரு சிறப்பு திட்டத்தை வகுத்தோம்; அது எங்கள் ஊரின் அருகே இருக்கும் வனத்தில் மரம் நடுதல்

5. `act=0.5878` `token='▁அப்பா'`  
   அப்பா மற்றும் நான் மட்டும் இரவு உணவைத் தவிர்க்கவில்லை, அது எங்களுக்கு சிறந்தது.

6. `act=0.5878` `token='▁அப்பா'`  
   அப்பா மற்றும் நான் கூடியே கணிதப்பாடத்தில் சிறப்பாக பயின்றோம்.

7. `act=0.5870` `token='▁심'`  
   심층 신경망은 비선형 매핑을 통해 데이터의 고차원적 구조를 효과적으로 모델링할 수 있다.

8. `act=0.5749` `token='▁지난'`  
   지난 회의에서 논의된 정책은 내부 검토를 거쳐 다음 달 시행 예정입니다.

## Candidate 5: feature 5680

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.918`
- validation effect: `-0.933`
- test effect: `-0.869`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.006`

### Top natural activations

1. `act=0.6249` `token='▁서'`  
   서장님, 현재 산림 자원의 지속 가능성을 보호하기 위해 지역 사회와의 협력을 바탕으로 한 자연 친화적 관리 방안을 도입하는 것이 매우 시급한 사항이라고 보고드립니다.

2. `act=0.6136` `token='▁Bem'`  
   Bem que eu poderia ter ido ao jogo se não tivesse chovido tanto naquela noite, mas como fiquei em casa, ainda me lembro de que você ligou para ver como eu estava.

3. `act=0.6136` `token='▁Bem'`  
   Bem, ele come, mas não cozinha nunca.

4. `act=0.6136` `token='▁Bem'`  
   Bem, acho que vale a pena discutir se a inteligência artificial ajudará a resolver os problemas ambientais ou agravará a crise.

5. `act=0.6086` `token='▁بيني'`  
   بيني سائق سيارتي أسرع مما يسمح به القانون.

6. `act=0.6086` `token='▁بيني'`  
   بيني ووالدتي في المطار كانت تتحفظ على سفري.

7. `act=0.6056` `token='▁저는'`  
   저는 사장님께 이번 출장 일정을 조율할 수 있도록 부탁드려도 되겠습니까?

8. `act=0.6056` `token='▁저는'`  
   저는 교수님께 연구 결과를 보고드렸습니다.

---

# Variable 17: animacy_and_humanness

- Original SAE evidence tier: **C**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.995**

## Candidate 1: feature 3104

- selection: `original_trainval_selected`
- train effect: `+0.499`
- validation effect: `+0.573`
- test effect: `+0.035`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.865`

### Top natural activations

1. `act=0.6566` `token='▁glass'`  
   My elderly neighbor took her daily vitamin supplement with a tall glass of warm milk after breakfast.

2. `act=0.6514` `token='▁iz'`  
   Ortaya atılan hafif topun yarışmacılar arasında geçmesi izleyicileri etkiledi.

3. `act=0.6506` `token='▁iz'`  
   Geratu daitezke arau horien arabera behin-behineko antolaketa batzuk egiten, parte-hartzaileen arteko komunikazioa izugarri zabaltzen duelarik.

4. `act=0.6505` `token='▁iz'`  
   Sona eriştiğimizde sahne kapalı oldu ama renkli kostümleriyle etkileyen oyunumuz izleyiciler arasında büyük bir yankı uyandırdı.

5. `act=0.6470` `token='▁iz'`  
   Futbol maçında bu kaleciyi ilk defa izliyorum ama çok çalıĢkandır heralde.

6. `act=0.6404` `token='▁iz'`  
   Bir sinema festivali izleyicilerine beklenmedik bir sürpriz sunmuştu.

7. `act=0.6393` `token='▁iz'`  
   Atletik maratonu kazanan sporcu, yarış boyunca koşusunu kusursuzce sürdüren tek kişi olarak, hem izleyicilerin takdirini topladı hem de jüri üyelerinin dikkatini çekti.

8. `act=0.6302` `token='▁iz'`  
   Bilim insanı, yeni geliştirilen teknolojiyi anlatırken izleyicilere dikkatle örnekler verdi.

## Candidate 2: feature 6618

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.500`
- validation effect: `+0.159`
- test effect: `+0.729`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.828`

### Top natural activations

1. `act=1.7096` `token='лект'`  
   Да, я видел новую технологию, которая использует искусственный интеллект для анализа биологических данных и позволяет учёным быстрее находить новые способы лечения редких заболеваний.

2. `act=1.7038` `token='能'`  
   ニューロンがシナプスを通じて情報を伝達する仕組みは、人工知能のネットワーク設計に大きな影響を与えた。

3. `act=1.6717` `token='▁बुद्धि'`  
   आधुनिक प्रौद्योगिकी के क्षेत्र में कृत्रिम बुद्धिमत्ता का विकास विज्ञान के कई क्षेत्रों को नए आयाम दे रहा है, जैसे कि चिकित्सा अनुसंधान में डेटा विश्लेषण और वातावरणीय मॉडलिंग में पूर्वानुमान सुधार।

4. `act=1.6165` `token='▁बुद्धि'`  
   विज्ञान और प्रौद्योगिकी के क्षेत्र में नवीनतम अनुसंधान ने जीव विज्ञान के क्षेत्र में कृत्रिम बुद्धिमत्ता के उपयोग के बारे में नए तथ्यों को प्रकाशित किया है।

5. `act=1.6148` `token='▁बुद्धि'`  
   विज्ञान और प्रौद्योगिकी के क्षेत्र में तेजी से विकास हो रहा है और अब एक से अधिक देशों में अंतरिक्ष अन्वेषण और कृत्रिम बुद्धिमत्ता के अनुसंधान को प्राथमिकता दी जा रही है।

6. `act=1.6095` `token='▁artifici'`  
   D'ici la fin de l'année scolaire prochaine, les établissements devront intégrer dans leurs programmes des modules spécifiques sur l'intelligence artificielle et sa place croissante dans l'éducation.

7. `act=1.6050` `token='能'`  
   山田先生は，人工知能の倫理的課題についての新たな研究が進んでいるとおっしゃっていたので，その説明をぜひ伺いたいと思っています。

8. `act=1.6015` `token='▁बुद्धि'`  
   आजकल विज्ञान और प्रौद्योगिकी के क्षेत्र में बड़े पैमाने पर प्रगति हो रही है, जिससे हम अब अंतरिक्ष अन्वेषण, कृत्रिम बुद्धिमत्ता और जीनोम इंजीनियरिंग जैसे क्षेत्रों में अद्भुत उपलब्धियाँ हासिल कर पा रहे हैं।

## Candidate 3: feature 10896

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.463`
- validation effect: `+0.355`
- test effect: `+0.376`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.680`

### Top natural activations

1. `act=1.3581` `token='▁#'`  
   项目文档需要按照最新版本的格式上传到共享文件夹，例如 "2023年度-Q4_KPI评估报告_v2.1.pdf"，并且在邮件主题中加上 #内部会议_11月9日 以便统一归档。

2. `act=1.3389` `token='▁#'`  
   Der Patient hat die Befunde unter dem Hashtag #FallID_45B12 auf der internen Plattform abgelegt.

3. `act=1.3350` `token='▁#'`  
   Am Montagabend stieß die Familie Meier-Steinberg auf den Hashtag #Familienfest2023, der die Einladung zur zentralen Feierlichkeit im Rathausplatz erklärte.

4. `act=1.3342` `token='▁#'`  
   Ich habe gerade die Datei „Rezepte_Oktober2023.pdf“ auf meinem Laptop gespeichert und sie gleich mit dem Hashtag #Sommergerichte getaggt.

5. `act=1.3198` `token='▁#'`  
   Die neuen Lehrpläne für das Gymnasium sind unter dem Hashtag #GymLehrplan2024 auf der offiziellen Schulhomepage einsehbar.

6. `act=1.3145` `token='▁#'`  
   After adjusting the parameters in the recipe file named `desserts_v4_2025.csv`, the system flagged several inconsistencies in the portion sizes listed under the `savory_sides` category using the hashtag #PortionMismatch.

7. `act=1.3098` `token='▁#'`  
   Ich habe gerade eine alte Hausaufgabe aus dem Ordner „Mathe_SS2023“ gefunden und sie online mit dem Hashtag #SchulzeitErinnerung geteilt.

8. `act=1.3082` `token='▁#'`  
   L'employé a envoyé un rapport détaillé intitulé "AnalyseQ4_2023_RH@departement.xlsx" à la direction via l'intranet, en incluant un commentaire avec le hashtag #ProjetsClés pour faciliter le suivi par l'équipe de gestion.

## Candidate 4: feature 3428

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.534`
- validation effect: `+0.138`
- test effect: `+0.583`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.921`

### Top natural activations

1. `act=1.5226` `token='vula'`  
   Mientras arreglaba el fogón de la cocina, le aseguré a mi hermana que el problema no era con el gas sino con la válvula que había instalado el fontanero hace unos meses.

2. `act=1.4733` `token='vula'`  
   El técnico revisó la válvula y comprobó que su funcionamiento era inadecuado.

3. `act=1.4283` `token='計'`  
   「今日は絶対に間に合うよ」と彼は自信満々に言い、時計をちらっと見ながら歩き出した。

4. `act=1.4078` `token='ör'`  
   Ortada duran büyük laboratuvar makinesi şu anda çalışıyor, çünkü sağdaki bilgisayar paneli ile solundaki sensörler arası veri aktarımı gerçekleşiyor.

5. `act=1.4074` `token='コン'`  
   電気を節約するために、エアコンの温度設定を上げることで、室温調節による電力消費量の増加を抑えることができる。

6. `act=1.4025` `token='コン'`  
   今日、会社の設備点検のために午後から出かけた際、いつもより気温が高く感じる中、新しく導入されたエアコンの冷房効果を実際に確認しました。

7. `act=1.4019` `token='вентилятор'`  
   Компьютер в гараже перегревается, поэтому сестра поставила вентилятор на стол и подключила его к блоку питания.

8. `act=1.3695` `token='ector'`  
   Quando o técnico ajustou os cabos, percebeu que faltava um conector essencial.

## Candidate 5: feature 2360

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.480`
- validation effect: `-0.835`
- test effect: `-0.151`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.883`

### Top natural activations

1. `act=1.1663` `token='▁الم'`  
   الله يعفو عن اللاعب المُتمسّك بفريقه رغم الهزائم المتكررة.

2. `act=1.0947` `token='▁الم'`  
   من المؤكد أن الطالب الموهوب في الفصل الدراسي الثاني سيعمل بجد أكبر مع المعلم الجديد لضمان حصوله على أعلى الدرجات في الامتحان النهائي، خاصة إذا كان يطمح للحصول على منحة دراسية بالخارج بعد تخرجه.

3. `act=1.0921` `token='▁ال'`  
   في ظل التطور المستمر في المجال التعليمي، تؤكد الجهات المختصة على أهمية توفير بيئة تعليمية آمنة ومحفزة تتناسب مع طبيعة الطالب الذكر أو الأنثى لضمان تطور شامل ومتوازن للمتعلمين على مستوى الشخصية والقدرات الأكاديمية.

4. `act=1.0759` `token='▁ال'`  
   جاء الألبوم الأول للفنان الشاب متضمّنًا أغنيات من ألحان مؤثرة ونصوص معبّرة جدًّا.

5. `act=1.0689` `token='▁ال'`  
   أحرز اللاعب الهدف الأول في الدقيقة الرابعة والعشرين من المباراة.

6. `act=1.0626` `token='▁ال'`  
   القى الفنان التشكيلي الضوء على تراث المنطقة من خلال لوحة مُدهشة.

7. `act=1.0293` `token='▁ال'`  
   الفنان التشكيلي الشهير محمد نجح في تنفيذ لوحة عملاقة تصور فيها فريق كرة القدم بلباسه الأحمر وهو يركض على الملعب تحت الشمس الذهبية بينما يصوب أحد اللاعبين الذين يرتدون زيًا أخضر نقيضًا إلى حارس المرمى الذي يرتفع قميصه الأسود من خلفه بسبب السرعة الكبيرة التي يتحرك بها.

8. `act=1.0293` `token='▁ال'`  
   الفنان الشاب يعرض لوحته الأولى في المهرجان الثقافي الدولي.

---

# Variable 18: person_marking_and_person_hierarchy

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.864**

## Candidate 1: feature 13235

- selection: `original_trainval_selected`
- train effect: `+0.378`
- validation effect: `+0.208`
- test effect: `+0.270`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.154`

### Top natural activations

1. `act=0.8266` `token='ము'`  
   నేము ఇంట్లో చలికాలంలో జలుబు ఏమి తగ్గలేదు.

2. `act=0.7933` `token='ము'`  
   మేము పసిడి నీరు గురించి మాట్లాడుతున్నాం.

3. `act=0.7933` `token='ము'`  
   మేము బయటకు వెళ్ళి ఈ అద్భుతమైన నక్షత్రాలు చూడాలనుకుంటున్నాం.

4. `act=0.7933` `token='ము'`  
   మేము ఈ సినిమాని చూడడం కోసం సర్వత్రా వచ్చాము, అయినప్పటికీ మీరు ఎలా వచ్చారో తెలియదు.

5. `act=0.7933` `token='ము'`  
   మేము ఆ జలపాతం చూడటానికి వెళ్లాం.

6. `act=0.7933` `token='ము'`  
   మేము వృక్షాలను రక్షించడానికి పాఠశాలలో కార్యక్రమం నిర్వహిస్తాము.

7. `act=0.7933` `token='ము'`  
   మేము ఆ బస్సులో వెళ్ళలేదు.

8. `act=0.7933` `token='ము'`  
   మేము గ్రామంలో వెళ్ళినప్పుడు మాతో సౌందర్యం నిండిపోయింది.

## Candidate 2: feature 4828

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.425`
- validation effect: `+0.401`
- test effect: `+0.302`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.138`

### Top natural activations

1. `act=1.6763` `token='▁जारी'`  
   राष्ट्रीय सुरक्षा के मुद्दे पर विदेश मंत्रालय ने एक बयान जारी करते हुए कहा कि वे आंतरिक खतरों के खिलाफ बल पैदा करने वाली सभी गतिविधियों पर नजर रखे रहेंगे।

2. `act=1.6177` `token='▁जारी'`  
   राष्ट्रपति ने एक बयान जारी किया।

3. `act=1.5384` `token='▁जारी'`  
   न्यूज़ चैनल ने बयान जारी करके मुद्दा साझा किया।

4. `act=1.4468` `token='▁जारी'`  
   मुख्यालय ने अधिसूचना जारी कर दी।

5. `act=1.3813` `token='▁जारी'`  
   सरकार ने अधिसूचना जारी कर दी।

6. `act=1.3805` `token='▁जारी'`  
   प्रशासन ने पेड़ों की कटाई रोकने का आदेश जारी किया।

7. `act=1.3739` `token='▁जारी'`  
   जम्मू कश्मीर में आज एक बड़ा राजनीतिक बयान जारी किया गया, जिसमें सरकार ने विशेष दर्जा कानून के बारे में अपनी नीति के पुनर्विचार पर गौर करने का वादा किया।

8. `act=1.3663` `token='▁जारी'`  
   सरकार ने नए कानून का अधिसूचना जारी कर दिया।

## Candidate 3: feature 14768

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.404`
- validation effect: `+0.416`
- test effect: `+0.374`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.087`

### Top natural activations

1. `act=1.1004` `token='en'`  
   Las películas animadas suelen explorar temas profundos que trascienden la infancia y resuenan con personas de todas las edades, mostrando una riqueza narrativa que a menudo sorprende al espectador más exigente.

2. `act=1.0243` `token='en'`  
   Bazekiten Poloen kanpoko bertanoan entrenatzen ari zirela.

3. `act=1.0180` `token='en'`  
   Dicen que las aves migran temprano por la niebla.

4. `act=1.0180` `token='en'`  
   Dicen que en la vida uno debe escuchar lo que el corazón quiere o seguir las reglas de la sociedad.

5. `act=1.0180` `token='en'`  
   Dicen que en las montañas se oyen sonidos extraños por la noche.

6. `act=1.0180` `token='en'`  
   Dicen que el mural que acaban de pintar en el centro cultural fue hecho por un grupo de artistas jóvenes que vienen de una pequeña ciudad del interior.

7. `act=1.0180` `token='en'`  
   Dicen que allí nació el vals vienés.

8. `act=1.0180` `token='en'`  
   Dicen que la selva es más fría de lo que parece.

## Candidate 4: feature 4252

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.390`
- validation effect: `-0.465`
- test effect: `-0.354`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.038`

### Top natural activations

1. `act=1.2138` `token='jára'`  
   El guía les advirtió al turista y a mí que no se alejáramos del grupo.

2. `act=1.2059` `token='ára'`  
   Aunque el entrenador sugirió que descansáramos un rato, decidimos seguir practicando para mejorar nuestra técnica.

3. `act=1.1993` `token='ení'`  
   Mientras paseaba por el barrio histórico, observé con sorpresa cómo los turistas se detenían frente a la fachada del antiguo teatro, admirando su fachada colorida y comentando emocionados sobre la representación que se celebraría allí esa noche.

4. `act=1.1949` `token='ára'`  
   Mientras jugábamos al fútbol en el parque, él nos gritó para que le pasáramos el balón, pero antes de que cualquiera de nosotros pudiera reaccionar, se lo quedó un niño más pequeño que acababa de llegar al campo.

5. `act=1.1671` `token='uva'`  
   S'il pleuvait demain, les plantes pousseraient mieux.

6. `act=1.1671` `token='uva'`  
   S'il pleuvait demain, je resterais chez moi.

7. `act=1.1671` `token='uva'`  
   S'il pleuvait encore, on ne pourrait pas continuer la randonnée.

8. `act=1.1671` `token='uva'`  
   S'il pleuvait, on resterait à la maison.

## Candidate 5: feature 8975

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.388`
- validation effect: `+0.185`
- test effect: `+0.305`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.711`

### Top natural activations

1. `act=0.9916` `token='▁ovat'`  
   Myrskikylmässä ovat voineet myrskyt meitä edeltä jyrkemmin kuin suvussa ollut perhe.

2. `act=0.9856` `token='▁представлены'`  
   Я смотрю на большую выставку современного искусства, где представлены коллективные работы разных художественных групп и каждая из них рассказывает свою историю через общее пространство галереи.

3. `act=0.9844` `token='▁помогают'`  
   У меня опять поднялась температура, не помогают ни таблетки, ни чай с лимоном, и вообще я чувствую себя ужасно, точно так же как вчера и позавчера.

4. `act=0.9788` `token='▁представлены'`  
   На большой и современной выставке, где представлены самые передовые технологии в области медицины, вниманию посетителей были предложены уникальные разработки, созданные командами из десятков стран мира.

5. `act=0.9684` `token='ются'`  
   Несмотря на то что в каждом ресторане города предлагаются блюда местной кухни, можно найти по крайней мере один заведение, где гостям подают традиционный суп из диких водорослей по старинным рецептам, переданным из поколения в поколение.

6. `act=0.9631` `token='действуют'`  
   Несмотря на то что в центре города действуют строгие ограничения на въезд для автомобилей, пешеходные зоны привлекают всё больше туристов и местных жителей, которые с удовольствием гуляют здесь по вечерам, не задумываясь о том, какие меры были приняты городскими властями для улучшения качества воздуха и безопасности движения.

7. `act=0.9514` `token='▁проходят'`  
   По вечерам в маленьких галереях города обычно проходят выставки молодых художников.

8. `act=0.9513` `token='▁прошли'`  
   В городе прошли первые выборы мэра.

---

# Variable 19: inclusive_exclusive_distinction

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.916**

## Candidate 1: feature 6062

- selection: `original_trainval_selected`
- train effect: `-0.854`
- validation effect: `-0.494`
- test effect: `-0.023`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `3.526`

### Top natural activations

1. `act=0.6282` `token='我'`  
   地铁站台边，我等车时，看着来来往往的上班族。

2. `act=0.6150` `token='我'`  
   走進圖書館，我看到有人正朝著閱覽區這邊來。

3. `act=0.6102` `token='我'`  
   在故宫文创商店里，我买到了一个印着#明永乐青花瓷028的笔记本。

4. `act=0.6066` `token='我'`  
   火车准时到达，我松了口气。

5. `act=0.6059` `token='我'`  
   在医院的走廊里，我看到一个护士正急匆匆地走向急诊室，手里拿着病历，脸上写满了焦急，而另一边的医生却刚刚从手术室出来，神情轻松，似乎刚完成了一台成功的手术。

6. `act=0.6046` `token='我'`  
   Çamaşırlarımı搜集完之前，我没法出去。

7. `act=0.5936` `token='我'`  
   办公室太吵，我根本没法集中。

8. `act=0.5909` `token='我'`  
   就在我们昨天到达的那座山脚下，远远就能看到车站附近的登山缆车缓缓上升，而近处我脚下的石阶却湿滑得让我不得不小心挪动脚步。

## Candidate 2: feature 10819

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.788`
- validation effect: `+0.716`
- test effect: `+0.517`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.556`

### Top natural activations

1. `act=1.1892` `token='▁un'`  
   Stunned relatives gathered in the dimly lit living room, exchanging uneasy glances as the long-lost cousin—whom they hadn’t seen since childhood—unexpectedly appeared on their doorstep just hours after receiving the unexpected call.

2. `act=1.1698` `token='▁un'`  
   After their mother explained the situation clearly, my cousins finally understood why their grandfather had insisted on visiting us unannounced last weekend.

3. `act=1.1690` `token='▁un'`  
   Each of the three senior team members submitted their individual reports along with the collective family action plan, ensuring that both the singular contributions and the unified goals were clearly addressed in the final documentation provided to the board.

4. `act=1.1640` `token='▁un'`  
   A good friend is someone who listens without judgment and offers support unconditionally.

5. `act=1.1585` `token='▁un'`  
   Despite the meticulously planned itinerary that accounted for every possible delay, the expedition was ultimately negated by the unforeseen closure of the mountain pass due to landslides caused by the region’s sudden and severe monsoonal rains.

6. `act=1.1549` `token='▁un'`  
   Despite assurances from local officials that no immediate threats were expected, many residents refused to return home, fearing that the unstable conditions might still result in unexpected complications.

7. `act=1.1534` `token='▁un'`  
   Were it not for the public outcry, the policy would have passed unchanged.

8. `act=1.1487` `token='▁un'`  
   After the storm passed, the trees stood bent but unbroken in the clearing where the lightning had split one trunk and left scorch marks across the grass without a single drop of rain touching the ground.

## Candidate 3: feature 4396

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.768`
- validation effect: `-0.189`
- test effect: `-0.023`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.406`

### Top natural activations

1. `act=1.0092` `token='記者'`  
   文化庁の担当者は、「この新プロジェクトについて具体的にどのように市民に説明する予定ですか」と記者から質問されたが、その場で答える代わりに「現在、全容を明らかにする段階ではないため、もう少し時間をいただきたい」と述べ、詳細な説明は今後改めて行うことを表明した。

2. `act=0.9999` `token='記者'`  
   「この食品の保存方法について、社長は『冷暗所で保管してください』と記者に答えた。」

3. `act=0.9923` `token='記者'`  
   「この理論は実験で確認された」と研究者は記者会見で述べたが、彼の言葉には確信が感じられなかった。

4. `act=0.9920` `token='記者'`  
   報道によると、市長は記者会見で新しい政策の導入を発表した。

5. `act=0.9892` `token='記者'`  
   「市長がこの件について公に謝罪した」と記者は伝えました。

6. `act=0.9876` `token='記者'`  
   院長先生は新型インフルエンザ対策について記者会見で重要な発表をされた。

7. `act=0.9864` `token='記者'`  
   「今後、地方自治体は環境に配慮した政策を積極的に推進していく予定です」と市長は記者会見で述べ、具体的な実施計画についても言及しました。

8. `act=0.9844` `token='▁journaliste'`  
   Le maire, accompagné de son équipe technique ainsi que des représentants des services municipaux concernés, a signé, devant les journalistes présents dans la salle et au terme d'une réunion marathon, l'arrêté municipal fixant les nouvelles règles d'urbanisme à respecter par tous les propriétaires.

## Candidate 4: feature 6385

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.762`
- validation effect: `-0.497`
- test effect: `-0.169`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.874`

### Top natural activations

1. `act=0.9260` `token='▁durch'`  
   Obwohl ich mir die Karte noch einmal angesehen hatte, landeten wir doch am falschen Bahnhof und mussten uns durchfragen, bis wir endlich den richtigen Zug fanden, der uns zum Konzert bringen sollte.

2. `act=0.9095` `token='▁durch'`  
   Wenn du morgen zum Treffen mit Kollegen und Vorgesetzten gehst, solltest du dich unbedingt gut vorbereiten und dir die wichtigsten Punkte noch einmal im Detail durchlesen.

3. `act=0.9060` `token='▁durch'`  
   Erst als sie den Bericht selbst durchgelesen hatte, wurde ihr die Bedeutung der Forschungsergebnisse wirklich klar.

4. `act=0.9030` `token='▁durch'`  
   Weil der Zug nach Salzburg über Stuttgart durchfuhr, machte sie einen Zwischenstopp am Bahnhof Hauptstadt mit ihren Großeltern und probierte das berühmte Stuttgarter Weisswurstfrühstück.

5. `act=0.9025` `token='▁durch'`  
   Als wir den Markt in Florenz durchstreiften, kauften sich die Kinder selbst ein Eis, während ich uns alle im Café gegenüber etwas zu trinken holte.

6. `act=0.8832` `token='▁durch'`  
   Mir ist aufgefallen, dass man die Protagonistin in dem Theaterstück fast immer durch "sie" anspricht, aber ihre eigene Stimme selten wirklich hört.

7. `act=0.8793` `token='▁durch'`  
   Macht den Touristen die Augen für die verborgenen Schönheiten der Altstadt auf, indem ihr mit ihnen durch schmale Gassen spaziert und das Flair der alten Marktplätze betont.

8. `act=0.8740` `token='▁durch'`  
   Er hat sich heute nach dem Frühstück eine kleine Pause gegönnt, um durchzuatmen.

## Candidate 5: feature 5487

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.832`
- validation effect: `+0.630`
- test effect: `+0.578`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.770`

### Top natural activations

1. `act=0.7840` `token='t'`  
   If you're looking for someone reliable in the office, you won't go far wrong with a team member who consistently meets deadlines.

2. `act=0.7763` `token='▁not'`  
   I think that sculpture might be made of bronze, but I’m not completely sure.

3. `act=0.7676` `token='▁नहीं'`  
   खिलौना कुत्ता वास्तविक कुत्ते की तरह नहीं भागेगा।

4. `act=0.7652` `token='▁not'`  
   She laughed and said, 'I'm not coming.'

5. `act=0.7639` `token='t'`  
   I wasn't sure if we needed to take the shuttle to the airport, but she said we could just walk there instead of catching one.

6. `act=0.7609` `token='▁not'`  
   It might be a virus, but I’m not sure.

7. `act=0.7601` `token='t'`  
   It was your turn to pick up the dry cleaning yesterday afternoon, wasn't it?

8. `act=0.7316` `token='t'`  
   She called yesterday but I wasn’t home.

---

# Variable 20: pronoun_richness_and_reduction

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 7551

- selection: `original_trainval_selected`
- train effect: `-0.823`
- validation effect: `-0.800`
- test effect: `-0.810`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.518`

### Top natural activations

1. `act=1.2860` `token='他'`  
   站在展览馆的入口处，他回想起十年前自己第一次参观时的激动心情。

2. `act=1.2684` `token='他'`  
   会议结束后，他向记者表示会尽快公布调查结果。

3. `act=1.2676` `token='他'`  
   展览开幕时，他正从展厅那头走来，手里拿着一叠设计图纸。

4. `act=1.2622` `token='他'`  
   在项目汇报会上，他强调了时间管理与团队协作的重要性，并展示了一份详细的工作进度表。

5. `act=1.2609` `token='他'`  
   站在广场中央，他回望着刚走过的石板路，转头又望向远处尚未到达的博物馆。

6. `act=1.2534` `token='他'`  
   这周末的羽毛球赛，他倒是没去。

7. `act=1.2457` `token='他'`  
   因此，他决定先洗个澡，然后吃点东西再继续工作。

8. `act=1.2445` `token='他'`  
   今天，天气晴朗，他，决定去公园散步。

## Candidate 2: feature 14161

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.828`
- validation effect: `-0.811`
- test effect: `-0.830`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.401`

### Top natural activations

1. `act=3.1880` `token='متد'`  
   بينما كان جدي الأكبر، وهو رجل متقدم في العمر وذو شخصية هادئة، يمارس عادة صباحية من التأمل بجانب حديقة عائلة خالته التي تبعد بضع كيلومترات عن قريتنا، أتى حفيده الأوسط، الذي درس الطب منذ سن مبكرة وله ذكاء فذّ، ليتحدث معه بلغة بسيطة لكنها صادقة ويُشاركه في الحديث عن ماضي العائلة الذي يمتد عبر عدة أجيال.

2. `act=3.0522` `token='▁سر'`  
   لما دخلت أمي الغرفة ووجّهت نظرها للنوايا المعروسة بالحبل، ضحكت بصوت مرتفع وقالت لأبي "ما إنك تصدق، ديّ حفنة أكياس بس قديمة مملوءة بخرابيش وبقايا شوكولاتة"، فرد أبوّا عليها بكل هدوء "وأنا أعرف، لكن البلاستيك ليه قيمة في قلب الأرامل"، فضحكا معًا وكأنهما يتفقان على سرٍّ

3. `act=3.0330` `token='錯'`  
   他一進門就看到我正在看手機，馬上走過來問我在找什麼，我就跟他說剛收到一個很有趣的訊息，是朋友群裡分享的冷知識，講的是人類大腦如何在無意識中處理語言資訊，這讓他馬上回應說是不是像翻譯時常會有的誤會，還舉出以前我們在學校討論中文和英文翻譯時他常犯的錯。

4. `act=3.0156` `token='قضي'`  
   لقد أعجبني تصميم الباحثة الشابة لمخطط توزيع الهواتف الذكية داخل المنازل، حيث استخدمت أداة تتبع التردد لفهم أفضل لأماكن استخدام كل عضو في العائلة للجهاز، وخلال عرضها قالت "هذا الجهاز يخص أخاك، فاجعله بعيدًا عن النوم ليلاً حتى لا يؤثر على نومك"، ثم شرحت كيف يمكن للوالدين مراقبة الأوقات التي يقضيها الأولاد في الاستخدام بطريقة تفاعل

5. `act=2.9775` `token='▁مح'`  
   إنَّ المديرَ المختصَّ بتنظيمِ الرحلاتِ العائليةِ قد أصدرَ توجيهاتهِ إلى فريقِ العملِ حول ضرورةِ مراعاةِ التكاليفِ والجدول الزمنيِّ لضمانِ وصولِ المسافرينَ إلى نقاطِ الوجهةِ المختلفةِ في أوقاتٍ محددةٍ، مع تأمينِ السبلِ المناسبةِ للراحةِ والنقاشِ المفتوحِ حول أيِّ تعديلٍ محتملٍ.

6. `act=2.9765` `token='▁الع'`  
   في الحيّ القديم، حيث تُحيط البيوت الأصيلة بالساحة مثل جذور شجرة عتيقة، يجلس العم أحمد على باب بيته المُنيب، مُحاطًا بالأحفاد الذين لا يكادون يفارقونه، بل ويطلبون منه دائمًا أن يروي لهم الحكايات التي كان يحدثها جدّهم الغامض، والذي لا يزال حاضرًا في ذاكرة العائلة رغم غياب جسمه منذ عقود.

7. `act=2.9603` `token='▁يت'`  
   في قرية صغيرة على ساحل البحر المتوسط حيث تربّت الأمهات بجيرانهن وتنادى الأطفال بأسماءٍ أحبوا سماعها في كل صباح، كانت تجلس الأسرة حول طاولة مفرومة من الخشب القديم، تبتسم الجدة وهي ترى القديم الجديد الذي نسجه الابن بأصابعه الطرية إلى جوار الحذاء المُستخدم الذي ظلّ صديقًا للطفلة الأولى، التي لم تبالِ بما يتطوّر فيه الزمن من

8. `act=2.9297` `token='▁الأ'`  
   في هذا المطعم الصغير الموجود بجانب الحديقة العامة، تقدم خدمة مميزة تحتوي على طبق شوربة الدجاج الدافئ واللذيذ مع طبق جانبي من الخضروات المطهية والجديدة، أو يمكنك اختيار إحدى الوجبات الكاملة التي تتكون من أرز بسمتي ودجاج مشوي ومخلل الخيار الطازج، حيث يحب المتعاملون معه من السكان المحليين والأجانب الزوار في كل الأوقات.

## Candidate 3: feature 6944

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.831`
- validation effect: `-0.860`
- test effect: `-0.788`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.261`

### Top natural activations

1. `act=1.5618` `token='▁он'`  
   Я никогда не говорил ему об этом, ведь он бы расстроился.

2. `act=1.4554` `token='▁он'`  
   Мама категорически отказалась позволить мне встречаться с этим парнем, потому что он уж слишком часто опаздывает, да ещё и не любит соблюдать чистоту в доме.

3. `act=1.4427` `token='▁ella'`  
   Claro que sí, voy a ayudar a mi hermana con su proyecto escolar porque ella me lo pidió anoche y además es una buena oportunidad para que nos llevemos mejor.

4. `act=1.4122` `token='▁er'`  
   Ich frage ihn, ob er mitkommen will, aber er sagt, dass er lieber zu Fuß geht.

5. `act=1.3875` `token='▁ellos'`  
   Es necesario que termines con los preparativos antes de que lleguen tus padres, ya que ellos tienen planeado cenar juntos como parte del acuerdo familiar que se estableció la semana pasada.

6. `act=1.3857` `token='▁он'`  
   Во время вечеринки я услышал, как тётя Нина сказала, что брат Пети купил новую машину, и она очень рада за него, потому что он мечтал о таком подарке много лет.

7. `act=1.3631` `token='▁он'`  
   Мама сказала, что папа не сможет прийти на семейный обед, потому что ему не разрешили взять отпуск, хотя он уже месяц просил об этом.

8. `act=1.3567` `token='▁él'`  
   La camiseta del equipo es de mi hermano, pero él ya no juega al fútbol.

## Candidate 4: feature 105

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.872`
- validation effect: `+0.888`
- test effect: `+0.891`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.233`

### Top natural activations

1. `act=4.3412` `token='▁వంట'`  
   మేము ఈ వంట చేసి అందరికీ పంచుకోడానికి సిద్ధంగా ఉన్నాము.

2. `act=4.2651` `token='व'`  
   हमारे कान ध्वनि के प्रति संवेदनशील होते हैं।

3. `act=4.2387` `token='▁प्रकल्प'`  
   मैंने अपने प्रबंधक से कहा कि उन्हें इस प्रकल्प के लिए विस्तार से रिपोर्ट तैयार करनी चाहिए।

4. `act=4.1552` `token='▁ebe'`  
   Okul, ebeveynlerin önerisine rağmen programı iptal etmedi.

5. `act=4.0954` `token='ோத'`  
   மாண்புமிகு முதல்வர், அவரது சகோதரர்களுடன் தமிழகத்தின் பொருளாதார முன்னேற்றம் குறித்து கூட்டம் நடத்தினார்.

6. `act=4.0920` `token='老師'`  
   教室裡老師說這裡的練習很重要，那裡的測驗更難。

7. `act=4.0891` `token='▁اقت'`  
   شاعری کے اس اقتباس میں، الفاظ کی ترتیب نے معنی کی گہرائی کو بدل دیا تھا۔

8. `act=4.0882` `token='▁öğretmenler'`  
   Okulun açılmasıyla birlikte hem öğretmenler hem de öğrenciler kendi rollerine geri dönerken öğretmenler, sınıftaki her öğrencinin velisine bilgi vermek ve süreci koordine etmek adına bir açıklama yazısı gönderdiler.

## Candidate 5: feature 11338

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.828`
- validation effect: `-0.800`
- test effect: `-0.691`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.179`

### Top natural activations

1. `act=1.1327` `token='は'`  
   この町の夏祭りは毎年のように熱気がすごいが、今年は特に人々の笑顔が輝いていて驚いた。

2. `act=1.1201` `token='は'`  
   その試合では、負けていたチームが最後の5分で流れを引き寄せる形で逆転勝ちを収め、観客席は歓声と拍手で満たされた。

3. `act=1.1099` `token='は'`  
   「このプロジェクトは家族の協力が不可欠だ」と彼女は再三述べていた。

4. `act=1.1099` `token='は'`  
   「このプロジェクトは来週までに完成させなければいけないんです、」と課長は説明して、部下たちに向かって追加の指示を出しました。

5. `act=1.1099` `token='は'`  
   「このプロジェクトは来週までに完了させる予定です。」とチームリーダーが説明してくれました。

6. `act=1.1099` `token='は'`  
   「このプロジェクトは来週までに終わります」と上司が言っていました。

7. `act=1.1099` `token='は'`  
   「このプロジェクトは来週までに完了させる必要があります。」

8. `act=1.1099` `token='は'`  
   「このプロジェクトは明日までに完了しなければならない」と彼は同僚に言い、みんなで締切りに向けて動き始めた。

---

# Variable 21: possession_and_alienability

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.980**

## Candidate 1: feature 9576

- selection: `original_trainval_selected`
- train effect: `+0.491`
- validation effect: `+0.516`
- test effect: `+0.508`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.221`

### Top natural activations

1. `act=1.9081` `token='▁letzten'`  
   Der Trainer betonte nochmals, dass die Mannschaft bis zum letzten Training alles geben müsse, um die Chancen auf den Meistertitel zu erhöhen.

2. `act=1.8568` `token='▁letzte'`  
   Erst nachdem sie das letzte Training erfolgreich absolviert hatte, durfte die junge Tennisspielerin im prestigeträchtigen Endspiel antreten.

3. `act=1.8425` `token='▁letzten'`  
   Sein ganzes Leben lang hat er um Vergebung gebeten, doch erst jetzt, mit dem letzten Brief seiner Schwester, fühlt er sich verstanden.

4. `act=1.8321` `token='▁letzten'`  
   Als sie den letzten Schluck ihrer wohltuenden Kamillentee trank, bemerkte sie, wie die Anspannung aus ihrem Körper wich und die sanfte Wärme im Bauch das Gefühl von Ruhe verbreitete.

5. `act=1.8321` `token='▁letzten'`  
   Als sie den letzten Spaten voll Erde in die Grabung warf, brachte sie dem jungen Hasen noch ein paar Karotten mit, die sie vorher beim Gemüsehändler am Markt besorgt hatte.

6. `act=1.8274` `token='▁letzte'`  
   Am Samstag um 9 Uhr fährt der letzte Zug in die Berge ab.

7. `act=1.8190` `token='▁last'`  
   No matter how many times I tried to plan the trip, there was always something that went wrong, and I ended up changing my schedule at the last minute just to find out it wasn’t worth the effort anyway.

8. `act=1.8080` `token='▁dernière'`  
   Personne ne voulait croire que ce voyage ne serait en rien un succès, mais ni les organisateurs, ni les participants, ni même les journalistes présents n’avaient imaginé qu’il serait annulé à la dernière minute.

## Candidate 2: feature 8666

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.627`
- validation effect: `-0.568`
- test effect: `-0.591`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.875`

### Top natural activations

1. `act=1.5530` `token='елка'`  
   На столе лежала большая чёрная тарелка с вкусным красным яблоком.

2. `act=1.5295` `token='ग'`  
   एक मनुष्य बस स्टैंड पर पैदल चल रहा था, जबकि उसके पास एक काला बैग भी था, जो वह अपने हाथ में पकड़े हुए था, और दूर से एक ट्रक आ रहा था जो

3. `act=1.4966` `token='투'`  
   그녀는 작은 빨강 봉투를 부치며 어머니가 화병을 챙겨 주길 원했다.

4. `act=1.4268` `token='ग'`  
   बस स्टॉप पर खड़े होकर देखा कि एक बच्चा अपनी माँ के साथ आता है जिसके हाथ में एक बैग भी है।

5. `act=1.4257` `token='तल'`  
   कार्यालय में एक कुत्ता बैठे शीशे की छोटी पानी की बोतल के सामने लिपटा था।

6. `act=1.3917` `token='ग'`  
   उसने अपनी माँ को स्टेशन पर एक छोटी बैग हरामन खरीदी।

7. `act=1.3902` `token='дан'`  
   Моя старая бабушка оставила мне в наследство старинный чемодан, который она всегда возила с собой в путешествиях.

8. `act=1.3893` `token='su'`  
   Arkadaşımın elinde kocaman bir çikolata-bisküvi kutusu vardı ve herkese içinden birer parça ikram ettiyordu.

## Candidate 3: feature 15325

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.525`
- validation effect: `+0.483`
- test effect: `+0.523`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.846`

### Top natural activations

1. `act=2.4700` `token='मा'`  
   दिल्ली से नौकरी करने मुंबई आया है मेरा भाई, वो अपने मामा के घर पर रहता है जिसके पास एक छोटा सा फ्लैट है।

2. `act=2.3705` `token='و'`  
   میاں تنویر علی نے اپنی بہو کو گھر سے نکال دیا۔

3. `act=2.3239` `token='मा'`  
   मेरी बहन के दो बच्चे हैं, और वे अपने मामा से बहुत प्यार करते हैं।

4. `act=2.3229` `token='దరు'`  
   నేను, నా సోదరుడు, నా స్నేహితుడు మరియు నా పెద్దలు కలిసి గ్రామంలో జరిగే సంక్రాంతి వేడుకల్లో

5. `act=2.3229` `token='దరు'`  
   నేను, నా సోదరుడు మరియు మా అమ్మ రేపు నగరంలోకి వెళ్తాం.

6. `act=2.3013` `token='దరు'`  
   నేను నా సోదరులతో కలిసి సంసారం నడుపుతాను కానీ మీరు మా తల్లితో కలిసి ఉన్నప్పుడు ఏమైనా చేయగలరు.

7. `act=2.2974` `token='e'`  
   Gure etxekidea bihurtu zen, bere semeak gogokoa egiten duen kantua entzuteko.

8. `act=2.2778` `token='e'`  
   Itzal zahar batek, udazka gainean pizten den lehen argi hustaurrea ikustean, antzinako gizonaren erreputabiltza naturaren sustraitzarekin lotzen ari zen narratzaileak esaldi bat errepikatzen zuen, berrogei urte ondoak pasatu ostean, bere seme-arrenaren eskuetan.

## Candidate 4: feature 7918

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.605`
- validation effect: `+0.546`
- test effect: `+0.366`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `10`
- specificity ratio: `0.665`

### Top natural activations

1. `act=3.3213` `token='▁y'`  
   Il me semble qu’avec la manière dont le projet avance actuellement, nous allons devoir revoir les échéances dans les semaines à venir, car il y a un retard significatif sur plusieurs tâches essentielles.

2. `act=3.3042` `token='▁y'`  
   Il a fallu que tout le monde répète plusieurs fois les consignes pour s'assurer que tout le monde les ait bien comprises, et même comme ça, il y avait encore des malentendus qui se sont accumulés au fil de la journée.

3. `act=3.2651` `token='▁key'`  
   A chef said that “the key to great soup is patience,” but he also emphasized how fresh ingredients matter most.

4. `act=3.2557` `token='y'`  
   Il n’a pas fallu que je m’adresse à lui pour qu’il comprenne ce qu’il devait faire, puisqu’on le lui avait déjà dit plusieurs fois par écrit, et il n’y avait vraiment aucune raison qu’il ne se mette pas au travail tout de suite.

5. `act=3.2330` `token='▁y'`  
   Je suis certain qu’il faut absolument engager un conseiller juridique avant de signer le nouveau contrat avec l’entreprise, car il y a trop de clauses floues qui pourraient nous causer des ennuis plus tard.

6. `act=3.2329` `token='▁en'`  
   La nouvelle recette qu’elle a inventée, avec des légumes fraîchement cueillis du jardin et une sauce au fromage fondant qui mettait en valeur leur goût naturel, fit sensation lors du dîner de famille et on en redemandait déjà à chaque plat suivant.

7. `act=3.2269` `token='▁y'`  
   Ce samedi matin-là, pendant que le match de foot retransmis à la télévision se déroulait depuis l’extérieur, nous étions plusieurs dans le salon, les yeux rivés sur l’écran et prêts à crier, à commenter, même si tout le monde savait déjà ce qui allait arriver, car on connaissait bien le jeu, les temps forts et les fautes répétées, mais on y allait quand même, comme d’habitude.

8. `act=3.2205` `token='▁key'`  
   Every afternoon around three, I can usually catch the janitor napping in his cart just outside the break room, the keys still dangling from his belt and the radio playing some old jazz tune he seems to enjoy.

## Candidate 5: feature 260

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.496`
- validation effect: `-0.535`
- test effect: `-0.301`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `11`
- specificity ratio: `0.541`

### Top natural activations

1. `act=1.5930` `token='▁logic'`  
   It's fascinating how quantum-computing architectures often borrow self-similar patterns from nature, like fractal geometries that somehow mirror the recursive logic needed for error correction in qubit operations.

2. `act=1.5593` `token='▁graduation'`  
   The parents will attend the graduation ceremony next week, where their daughter has been accepted into a prestigious university program after years of hard work and dedication.

3. `act=1.5588` `token='▁change'`  
   With growing public concern over the policy change, officials emphasized transparency during today’s press briefing.

4. `act=1.5372` `token='▁life'`  
   The lifeguard tossed the swimmer a float.

5. `act=1.5189` `token='▁policy'`  
   They proposed revising the policy after public feedback raised concerns.

6. `act=1.5170` `token='▁revision'`  
   Given the preliminary findings from the recent study and the fact that most students demonstrated improved test scores after the curriculum revision, it seems likely that the updated instructional approach has contributed significantly to enhanced academic performance across the department.

7. `act=1.5167` `token='ment'`  
   The university awarded every graduate a certificate during the commencement ceremony.

8. `act=1.5139` `token='▁policy'`  
   Researchers question whether the policy will improve public access to data.

---

# Variable 22: tense_prominence

- Original SAE evidence tier: **D**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.844**

## Candidate 1: feature 1385

- selection: `original_trainval_selected`
- train effect: `-0.396`
- validation effect: `-0.138`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.941`

### Top natural activations

1. `act=1.6058` `token='▁mes'`  
   Mi hermana siempre ha tenido muy buena salud, pero últimamente se siente cansada y ya no tiene el mismo apetito que antes, así que ayer fue al médico por recomendación de su jefe, quien también tuvo síntomas similares hace un mes.

2. `act=1.5852` `token='▁week'`  
   As I sat at the kitchen table sipping my coffee and reading the morning paper, a news headline caught my eye saying, “Scientists have discovered a new method to recycle old smartphones more efficiently,” which reminded me of what my brother had mentioned last week—that engineers are constantly finding smarter ways to reuse technology and reduce waste.

3. `act=1.5534` `token='去年'`  
   我坐在图书馆角落的窗边，看着外面的人群，忽然想起去年在这里备考时的紧张与期待。

4. `act=1.5396` `token='▁meses'`  
   El tratamiento que sigue mi hermano es el mismo que le recomendaron al doctor hace unos meses.

5. `act=1.5083` `token='前'`  
   据报道，该官员在上周的会议上表示，目前的情况与几个月前相比已经发生了显著变化。

6. `act=1.4997` `token='em'`  
   Der Lehrer erklärte den Schülern, dass sie im nächsten Jahr Physiklabor praktizieren werden, wie er es vor Kurzem erwähnt hatte.

7. `act=1.4848` `token='▁Monat'`  
   Wenn man sich die Ergebnisse der Simulationen ansieht, die wir vor einem Monat durchgeführt haben, zeigt sich, dass die neuen Algorithmen eine deutlich bessere Konvergenz aufweisen als die bislang verwendeten Methoden.

8. `act=1.4780` `token='▁días'`  
   Este algoritmo funciona mejor que el anterior que probamos hace unos días.

## Candidate 2: feature 1760

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.448`
- validation effect: `+0.352`
- test effect: `+0.372`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.927`

### Top natural activations

1. `act=0.7760` `token='▁Anke'`  
   Obwohl sie die Älteste war, kümmerte sich Anke stets um ihre jüngeren Geschwister.

2. `act=0.7305` `token='▁Javier'`  
   A pesar de que su hermana menor insistió en mudarse con ella, Javier prefirió darle tiempo para que decidiera por sí misma.

3. `act=0.7298` `token='▁Ali'`  
   Spor salonuna yeni başlayan Ali, kısa sürede ritimini buldu.

4. `act=0.7072` `token='▁Mathi'`  
   Alors qu'elle avait hésité à préciser qu'elle s'appelait Mathilde lorsqu'elle avait répondu au message, elle finit par ajouter son nom, pensant que cela ferait plus poli.

5. `act=0.7069` `token='▁Giulia'`  
   Mentre si stava riposando sul divano dopo la visita dal medico, a Giulia improvvisamente è venuta un'idea per migliorare il proprio stato di salute con rimedi naturali.

6. `act=0.7063` `token='▁Ali'`  
   Ofisimizde geçen hafta alınan masa, artık Ali'nin sorumluluğuna geçti ve artık projemiz için herkesin daha rahat çalışabileceği yeni düzenin bir parçası oldu.

7. `act=0.7024` `token='▁Ali'`  
   Yağmurun aralıksız yağdığı için, Ali parktaki etkinliğin iptal edildiğini duyurdu.

8. `act=0.6986` `token='▁Gem'`  
   Wenn es um Gemüse geht, helfen Ofengeräte meist am besten, die Konsistenz zu erhalten.

## Candidate 3: feature 11740

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.378`
- validation effect: `+0.052`
- test effect: `-0.060`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.914`

### Top natural activations

1. `act=0.7949` `token='▁más'`  
   La señora que vive en el tercer piso y cuida de sus tres gatos desde hace años acaba de comprar una camita nueva para el más joven, porque el más viejo ya no quiere saltar y prefiere quedarse quieto bajo la mesa de la cocina.

2. `act=0.7804` `token='▁mayor'`  
   The woman, who is the daughter of the mayor, has been appointed to the council by her father.

3. `act=0.7707` `token='▁mayor'`  
   In a press briefing held yesterday afternoon, the mayor confirmed that the city council had voted unanimously to increase funding for public transportation services starting next fiscal year.

4. `act=0.7615` `token='▁mayor'`  
   For the mayor’s speech, both the podium and the microphone were set up outside city hall.

5. `act=0.7615` `token='▁mayor'`  
   At the press conference yesterday, the mayor formally announced the new policy and reiterated that it would take effect immediately.

6. `act=0.7535` `token='▁mayor'`  
   At the summit, the mayor finally addressed the housing crisis.

7. `act=0.7498` `token='▁mayor'`  
   The committee approved the new policy, which was subsequently endorsed by the mayor.

8. `act=0.7495` `token='▁mayor'`  
   Strangely enough, the mayor's sudden resignation has left everyone confused and uneasy.

## Candidate 4: feature 8134

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.407`
- validation effect: `+0.488`
- test effect: `+0.395`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.710`

### Top natural activations

1. `act=1.6270` `token=','`  
   Однажды, гуляя по узкому лесному оврагу в предгорьях Крыма, я услышал странный щелчок и запахло горным цветом, который обычно растёт на вершинах, а не в тенистых местах.

2. `act=1.6147` `token=','`  
   Hier soir, en parcourant les pages du journal local, j'ai lu un article sur l'importante décision prise par le maire, une femme dynamique et engagée, concernant la rénovation des rues principales de notre petite ville.

3. `act=1.5813` `token=','`  
   Однажды, путешествуя на старом велосипеде по пыльной трассе, я заметил, как птица сидела на крыше кемпера, притормозившего у обочины, а рядом с ним стоял высокий юноша и безмолвно смотрел на горизонт.

4. `act=1.5740` `token=','`  
   Hier soir, en marchant dans le parc ombragé où des arbres imposants bordent les allées de gravier, j’ai remarqué que plusieurs feuilles jaunes, répandues çà et là, formaient un tapis épais sur le sol humide, et qu’un oiseau, perché sur une branche recourbée, chantait avec une douceur telle qu’elle semblait s’accorder parfaitement à la tranquillité du paysage automnal.

5. `act=1.5622` `token=','`  
   Работая над оформлением выставки современного искусства в маленькой галерее на окраине города, директор был глубоко тронут дативной симпатией к молодому художнику, чьи картины пронзали сердце зрителя своей невероятной чувствительностью и откровенностью.

6. `act=1.5507` `token=','`  
   Однажды, гуляя по родному сёлку, я вспомнил, как бабушка, улыбаясь, рассказывала о своих детях, и мне вдруг стало понятно, что семейные связи не просто кровные узы, а особый язык, который читается по взгляду, жесту и даже молчанию.

7. `act=1.5493` `token=','`  
   Al visitar el laboratorio espacial en Toulouse, nos sorprendió ver que él mismo supervisaba los datos recientes de Marte.

8. `act=1.5273` `token=','`  
   Enquanto caminhava pela feira cultural aberta em pleno centro da cidade, ouvi um grupo de jovens músicos tocar samba com tamanha paixão que parecia que a alegria de cada nota invadia os corações dos presentes.

## Candidate 5: feature 14496

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.461`
- validation effect: `+0.374`
- test effect: `+0.349`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `4`
- specificity ratio: `0.713`

### Top natural activations

1. `act=1.0423` `token='▁Elena'`  
   After her mother insisted she invite the neighbors for dinner, Elena persuaded her younger brother to prepare a few extra dishes just to make sure everyone would feel welcome.

2. `act=1.0404` `token='▁Иван'`  
   В понедельник утром Иван, привыкший к своему джипу, сел в автобус, который ехал медленно, но был самым удобным для поездки до вокзала, где он собирался проститься с подругой, уезжающей на год за границу.

3. `act=1.0354` `token='▁Иван'`  
   Виждам по лицето на Иван, че е ядосан, без да съм чувал лично какво го разстройва – сигурно е заради неразбраната задача от училище.

4. `act=1.0244` `token='▁Sarah'`  
   I heard from the coach that Sarah won the regional championship last weekend.

5. `act=1.0210` `token='▁Иван'`  
   След като разговарях с Ивана и със Стефан, разбрах какво всъщност е станало.

6. `act=1.0210` `token='▁Julie'`  
   Quand elle rentra chez elle après une journée fatigante au travail, Julie trouva que son mari avait rangé les affaires qu'elle laissait toujours éparpillées sur la table de la cuisine.

7. `act=1.0195` `token='▁Sarah'`  
   After checking the weather forecast and reviewing the travel itinerary, Sarah told her colleague that she had decided to postpone the trip since the local report mentioned heavy rain and possible flooding on the main route they were planning to take.

8. `act=1.0130` `token='▁Sarah'`  
   I heard through the office grapevine that Sarah was offered a promotion last week, though she hasn't confirmed it herself.

---

# Variable 23: aspect_and_event_structure

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.404**

## Candidate 1: feature 6216

- selection: `original_trainval_selected`
- train effect: `-0.705`
- validation effect: `-0.259`
- test effect: `+0.291`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.877`

### Top natural activations

1. `act=1.5053` `token='▁managing'`  
   Here on the third floor, managing the budget has been a bit of a headache since we reorganized last month.

2. `act=1.4594` `token='ing'`  
   After she measured out the flour, sugar, baking powder, and a pinch of salt, she made sure there were exactly four mixing bowls ready for the different colored batter she planned to pour into the muffin tins.

3. `act=1.4447` `token='▁spreading'`  
   Beneath the old oak’s spreading branches by the riverbank, we laid out a picnic cloth and shared stories of the seasons past.

4. `act=1.4440` `token='▁connecting'`  
   After missing the connecting flight due to a delayed train, she had to stay overnight in the city.

5. `act=1.4310` `token='ing'`  
   In the Arctic, melting sea ice continues to threaten native wildlife habitats.

6. `act=1.4302` `token='ing'`  
   None of the vending machines worked during the long security line at the airport.

7. `act=1.4254` `token='ing'`  
   The vending machine was reported out of service just as the last flu shot clinic was winding down.

8. `act=1.4236` `token='▁connecting'`  
   If I hadn't missed that connecting flight, I'd be home by now.

## Candidate 2: feature 4874

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.693`
- validation effect: `-0.239`
- test effect: `+0.296`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.475`

### Top natural activations

1. `act=1.6518` `token='▁testing'`  
   The engineers were testing the new software module when the system crashed.

2. `act=1.5197` `token='▁rolling'`  
   It might rain later, judging by how thick the clouds have been rolling in all afternoon.

3. `act=1.4920` `token='▁baking'`  
   They had been baking the bread since dawn, yet it will not be ready until after the sunset.

4. `act=1.4822` `token='▁baking'`  
   Right there on the counter was the pie she had been baking all morning.

5. `act=1.4787` `token='▁doing'`  
   We planted tomatoes in the garden last spring and they’ve been doing well since.

6. `act=1.4177` `token='ing'`  
   Yesterday afternoon, my dad was fixing the fence while my brother was mowing the lawn, and they were both done before dinner time.

7. `act=1.4075` `token='ving'`  
   After checking the weather forecast and realizing it was going to be rainy all weekend, we decided not to go hiking and instead stay home and try that new board game everyone’s been raving about.

8. `act=1.3836` `token='▁baking'`  
   I wonder if the cake will be ready by the time everyone gets here, considering how long it's been baking and the way the kitchen smells like cinnamon and vanilla.

## Candidate 3: feature 701

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.706`
- validation effect: `-0.279`
- test effect: `+0.358`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.771`

### Top natural activations

1. `act=0.7925` `token='▁три'`  
   Жители деревни собрали триста килограммов яблок и развезли их по соседним сёлам.

2. `act=0.7715` `token='▁собра'`  
   Все родственники собрались вместе, чтобы обсудить семейный устав и традиции.

3. `act=0.7543` `token='▁собра'`  
   В выходной день вся семья собралась на кухне, чтобы вместе приготовить завтрак и обсудить планы на предстоящую неделю.

4. `act=0.7520` `token='▁три'`  
   Согласно расписанию, поезд должен был прибыть в три часа, но из-за непредвиденных обстоятельств он не только опоздал на несколько часов, а вообще перенесён на завтра.

5. `act=0.7363` `token='▁собра'`  
   Во время семейного торжества все родственники собрались вместе, чтобы поздравить старших детей с первым днём в школе, а младшего — с тем, что он наконец-то научился ходить без поддержки.

6. `act=0.7331` `token='▁собра'`  
   Все члены семьи собрались вместе, чтобы отпраздновать день рождения дедушки, и каждый внес свой вклад в подготовку торта.

7. `act=0.7328` `token='▁собра'`  
   Все члены семьи собрались в гостиной, чтобы вместе посмотреть спектакль.

8. `act=0.7328` `token='▁собра'`  
   Все члены семьи собрались вместе, чтобы обсудить планы на семейную поездку.

## Candidate 4: feature 13189

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.695`
- validation effect: `-0.026`
- test effect: `+0.502`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.727`

### Top natural activations

1. `act=1.5208` `token='est'`  
   Il y a une valise qui n'est plus à elle depuis qu'elle a déménagé.

2. `act=1.4988` `token='▁est'`  
   Le joueur a glissé sur la pelouse et est tombé à la renverse.

3. `act=1.4802` `token='▁est'`  
   Je pense qu’elle a dû laisser son parapluie à la maison parce qu’elle est rentrée mouillée.

4. `act=1.4800` `token='est'`  
   Personne n’aime la pollution, n’est-ce pas ?

5. `act=1.4799` `token='▁est'`  
   Le dîner que j’avais préparé pour fêter mon anniversaire avec mes amis a été complètement gâché par la sonnette d’un livreur qui est arrivé au mauvais moment.

6. `act=1.4749` `token='▁est'`  
   La cuillère, qui est en inox, se trouve dans le tiroir à côté des fourchettes.

7. `act=1.4648` `token='▁est'`  
   Il me l’a prise sans que je m’en aperçoive et est parti en courant vers la pharmacie comme s’il connaissait exactement ce qu’il devait chercher.

8. `act=1.4638` `token='▁est'`  
   Il a suggéré que sa collègue prenne en charge le projet, car elle est plus expérimentée dans ce domaine.

## Candidate 5: feature 10398

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.655`
- validation effect: `-0.243`
- test effect: `+0.496`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.705`

### Top natural activations

1. `act=1.8618` `token='▁will'`  
   They had been baking the bread since dawn, yet it will not be ready until after the sunset.

2. `act=1.8186` `token='▁will'`  
   I have noticed that whenever my mother bakes a batch of her famous cinnamon rolls, she always makes twice as many as needed, so there will certainly be plenty left for everyone in the house, including those who might not even be home yet but are expected for dinner.

3. `act=1.7879` `token='▁will'`  
   The mayor announced at the press conference that, "We will implement new policies to improve public transportation by next summer," which drew applause from the audience.

4. `act=1.7864` `token='▁will'`  
   The manager reviewed the report yesterday and will present it at the meeting today.

5. `act=1.7716` `token='▁will'`  
   The mayor announced at the press conference, "We will hold a public meeting next week to address the concerns about the new development."

6. `act=1.7457` `token='▁will'`  
   It’s definitely true that she will attend the meeting if we confirm her schedule by noon, so we should send the official invitation right away and let her know how important her presence is for the discussion.

7. `act=1.7382` `token='▁will'`  
   He explained the theory yesterday and will continue today, moving through each stage clearly.

8. `act=1.7321` `token='▁will'`  
   The train left the station on time and will arrive at the next city just before sunset.

---

# Variable 24: modality_and_mood

- Original SAE evidence tier: **C**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.920**

## Candidate 1: feature 3941

- selection: `original_trainval_selected`
- train effect: `+0.483`
- validation effect: `+0.208`
- test effect: `+0.141`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.194`

### Top natural activations

1. `act=1.0815` `token='▁deben'`  
   Todos los viajeros deben pasar por al menos una revisión de seguridad antes de abordar el avión.

2. `act=1.0775` `token='▁debe'`  
   Todo estudiante del programa universitario debe cursar al menos una asignatura de ciencias sociales y otra de ciencias exactas, para garantizar que todos hayan adquirido conocimientos básicos en ambos campos antes de graduarse.

3. `act=1.0570` `token='▁debe'`  
   El viajero debe asegurarse de que su equipaje esté etiquetado claramente antes de abordar el avión.

4. `act=1.0569` `token='▁debe'`  
   En el aeropuerto internacional de Madrid, cada viajero debe mostrar su pasaporte y tarjeta de embarque al personal aduanero y de seguridad.

5. `act=1.0520` `token='▁debe'`  
   Todo empleado debe cumplir con al menos una norma de seguridad.

6. `act=1.0451` `token='▁debe'`  
   Cada atleta debe completar tres series de cinco ejercicios distintos.

7. `act=1.0436` `token='▁deben'`  
   Todos los ciudadanos deben pagar impuestos según sus ingresos.

8. `act=1.0433` `token='▁debe'`  
   Cada empleado del departamento de logística debe coordinar con al menos un representante de cada sección para garantizar que todos los materiales lleguen antes del comienzo de la reunión mensual.

## Candidate 2: feature 13197

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.616`
- validation effect: `+0.423`
- test effect: `+0.444`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.055`

### Top natural activations

1. `act=1.3041` `token='▁to'`  
   You really ought to water the plants before heading out, even if it's raining later, just to be sure they're well-moistened for the dry spell ahead.

2. `act=1.2602` `token='▁debes'`  
   Si me pasas un minuto, te cuento algo importante que no debes perder de vista.

3. `act=1.2300` `token='▁should'`  
   The doctor explained that you really should take the prescribed medication regularly and attend all follow-up appointments to ensure full recovery from the infection.

4. `act=1.1901` `token='▁should'`  
   You really should take the time to wash your hands before eating, especially after being outside all day and touching things like door handles and public transit poles.

5. `act=1.1901` `token='▁should'`  
   You really should take your medication as prescribed by the doctor.

6. `act=1.1779` `token='▁to'`  
   You ought to respect your parents' wishes.

7. `act=1.1730` `token='▁debemos'`  
   Claro que no es cierto que los algoritmos de aprendizaje automático no puedan mejorar con más datos de alta calidad, pero tampoco debemos creer que todo avance tecnológico resuelva todos nuestros problemas sociales de un día para otro.

8. `act=1.1555` `token='▁pas'`  
   Vous savez, docteur Lambert, même si vous êtes très gentil avec nous, il ne faut pas toujours vous tutoyer quand on parle à des patients inconnus, surtout s’ils ont une certaine position sociale ou appartiennent à une famille influente.

## Candidate 3: feature 2105

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.524`
- validation effect: `-0.381`
- test effect: `-0.154`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.010`

### Top natural activations

1. `act=0.9115` `token='▁the'`  
   In many cultures, folk tales serve as mirrors reflecting the values and fears of entire communities.

2. `act=0.9064` `token='▁the'`  
   In many cultures, art reflects the values that shape society.

3. `act=0.8943` `token='▁the'`  
   It is widely believed that the most profound forms of learning emerge not through rigid instruction but via experiences that engage the senses, evoke emotional resonance, and reflect the cultural narratives embedded in art and music.

4. `act=0.8632` `token='▁the'`  
   If the algorithm processes the input data correctly, it will generate a predictive model that accurately reflects the observed patterns in the dataset.

5. `act=0.8513` `token='▁la'`  
   Las montañas altas y los ríos fríos del norte alimentan bosques densos y húmedos que reflejan la fuerza silenciosa de la naturaleza en constante transformación.

6. `act=0.8410` `token='▁the'`  
   A sculpture represents the idea that art captures the essence of human experience through form and material.

7. `act=0.8361` `token='▁su'`  
   Las antigas murallas de la ciudad se encuentran cubiertas de murales que reflejan su rica historia.

8. `act=0.8309` `token='▁the'`  
   Critics argue that the film, though beautifully shot, doesn't quite capture the essence of the original play.

## Candidate 4: feature 6645

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.525`
- validation effect: `+0.570`
- test effect: `+0.022`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.875`

### Top natural activations

1. `act=1.5134` `token='▁haga'`  
   Es muy importante que hagas ejercicio con regularidad para mantener la salud.

2. `act=1.5013` `token='ble'`  
   Es necesario que el jefe hable con los empleados sobre cómo mejorar la comunicación en la oficina para evitar malentendidos y trabajar mejor en equipo.

3. `act=1.4901` `token='▁participe'`  
   É fundamental que os alunos participem ativamente das discussões em sala de aula.

4. `act=1.4867` `token='▁haga'`  
   Es fundamental que el paciente lo haga como se le indica para evitar complicaciones graves.

5. `act=1.4821` `token='▁siga'`  
   Aunque es fundamental que el paciente siga las indicaciones del médico con respecto al medicamento y la dosis, es común observar en clínicas rurales que algunos olvidan completar su tratamiento, lo que puede provocar recaídas o resistencias bacterianas difíciles de controlar.

6. `act=1.4692` `token='▁analise'`  
   É necessário que analisemos os dados antes de enviar o relatório ao cliente.

7. `act=1.4538` `token='▁participe'`  
   Es necesario que el hermano menor participe en la decisión final, aunque no esté del todo de acuerdo con su tío.

8. `act=1.4382` `token='che'`  
   Il est essentiel qu’un chef de projet sache écouter activement ses équipes pour favoriser une communication claire et efficace dans un environnement professionnel exigeant.

## Candidate 5: feature 4257

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.568`
- validation effect: `+0.529`
- test effect: `+0.391`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.779`

### Top natural activations

1. `act=1.2711` `token='.'`  
   Sosyal medya üzerinden yapılan açıklamada, internet sitelerinde yer alan yasa dışı içerikleri gerekli kurumlara bildirmenin vatandaşlık görevi olduğu ve bu durumun hukuku açısından da önemli olduğu belirtilerek, bu tür davranışların anayasa ve yasalara uygun şekilde yapılmaması gerektiğine dikkat çekildi.

2. `act=1.2378` `token='.'`  
   Lurralde bateko biztanleek etorkizuneko udal paretak multzoan egindako azterketen arabera, komunikazioarekin zerikusia duten ondasun teknologiko berriek ezagutzaren garapena eta elkarlanean trebetasuna hobetzen lagunduko litezke, besteak beste, jende gehiago ezartu eta informazio gehiago eskuratzea lortuz herriko egiatan parte hartzen dutenetatik.

3. `act=1.2291` `token='.'`  
   Gelişim gösteren iller listesinde yer alan Afyonkarahisar'da eğitimde doğrudan gözlemler ve okul ziyaretleriyle elde edilen verilere göre, öğretmenlerin mesleki gelişim programlarına katılmasıyla öğrencilerin başarı oranlarında önemli artışlar kaydedildiği saptandı.

4. `act=1.2138` `token='.'`  
   ABD Dışişleri Bakanlığı, Türkiye'nin Suriye'deki durum ile ilgili yaptığı açıklamalarda daha durağan bir tavır sergilemeyi tercih ederken, Rusya ile yapılan istişarelerin ardından bazı diplomatik iletişim kanallarının yeniden açılması yönünde sinyaller verildiğini açıkladı.

5. `act=1.2092` `token='.'`  
   Yargıç, zabittin raporuna dayanarak çocuğun psikolojik durumunun iki ebeveyn arasında dengesiz dağıldığını, baba tarafının da ana velayetini devralmasının çocuk için olumsuz olabileceğini belirterek kararını açıkladı.

6. `act=1.2008` `token='.'`  
   İkili diplomatik ziyaretin ardından sivil toplum kuruluşları ve kamuoyunun tepkilerini değerlendiren dışişleri bakanı, iki ülkenin tarihi bağlarını güçlendirme konusunda mutabık kaldıklarını ve bunun ekonomi, eğitim ve altyapı projeleri üzerinden etkili bir iş birliğine dönüşebileceğini söyledi.

7. `act=1.1809` `token='.'`  
   Gizarteak ospitalerako lehen aplikazioa egiteko helburua duen politikaren ondorioz, soro-sistema publikoak gehiago jasango ditu entrenatutako mediku berriek, neurri hori dela eta espero den kualitate txarrarekin prestatzen diren pribatuen bost aldiz gehiago ematen dituzten zerbitzuak izango dituela uste dute.

8. `act=1.1772` `token='.'`  
   Kamudaki yeni çalışma yapısının uygulamasıyla birlikte tüm projelerin öncelikli olarak sonuçlarının değerlendirilmesi ve daha sonra planlama safhasına alınması yönünde açıklamalarda bulunan bakan, çalışanların önerilerinin kurumsal politikalara entegre edilerek her aşamada göz önünde bulundurulduğuna dair vurgu yaptı.

---

# Variable 25: epistemic_modality

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.931**

## Candidate 1: feature 15221

- selection: `original_trainval_selected`
- train effect: `+0.770`
- validation effect: `+0.566`
- test effect: `+0.590`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.198`

### Top natural activations

1. `act=1.5186` `token='▁doute'`  
   Dans le jardin, c’est précisément le rosier qui a poussé plus dru cet été, sans doute à cause de la pluie abondante et des soins constants que lui ont prodigués ma mère et moi.

2. `act=1.3639` `token='▁vielleicht'`  
   Die Vögel über dem stillen Moor sangen heute Morgen länger und lebhafter als gewöhnlich, vielleicht weil das letzte Regenwetter die Blüten in den Wäldern frischere Nektar spendete und so die ganze Natur zum Leben erwachte.

3. `act=1.3561` `token='▁perhaps'`  
   It seems that the leaves are turning earlier this year, perhaps due to the unusually warm autumn we've been experiencing.

4. `act=1.3433` `token='être'`  
   Il semble que les élèves aient mieux compris le sujet cette fois-ci, peut-être parce que l’explication donnée par la professeure s’est appuyée sur des exemples concrets tirés de leur quotidien, ce qui facilite généralement l’assimilation des notions abstraites en cours.

5. `act=1.3306` `token='▁vielleicht'`  
   Heute Abend schaue ich eine Dokumentation über die Politik im Bundestag, vielleicht möchtest du das auch mal sehen.

6. `act=1.3179` `token='▁quizás'`  
   Aunque el termostato indicaba que la casa estaba a 25 grados, seguía sintiendo frío después de regresar del laboratorio, quizás por el viento helado que entraba por la ventana entreabierta.

7. `act=1.3162` `token='être'`  
   C’est bizarre, mais il me semble qu’on a acheté deux boîtes de pâtes chaque fois qu’on passait au supermarché cette semaine, et pourtant on n’en a mangé que trois bols à dîner, donc j’ai peut-être compté trop vite ou alors on en a donné un reste à Lisa.

8. `act=1.3141` `token='▁doute'`  
   Il reste des livres sur la table, sans doute oubliés par le dernier visiteur.

## Candidate 2: feature 8920

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.605`
- validation effect: `+0.291`
- test effect: `+0.532`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.620`

### Top natural activations

1. `act=0.6812` `token='▁influ'`  
   La masa fermentada con levadura seca rápida y harina de trigo integral produce un pan crujiente con una corteza dorada, mientras que añadir mieles o azúcar moreno puede influir en el sabor dulce del interior esponjoso.

2. `act=0.6446` `token='▁مح'`  
   إنَّ المديرَ المختصَّ بتنظيمِ الرحلاتِ العائليةِ قد أصدرَ توجيهاتهِ إلى فريقِ العملِ حول ضرورةِ مراعاةِ التكاليفِ والجدول الزمنيِّ لضمانِ وصولِ المسافرينَ إلى نقاطِ الوجهةِ المختلفةِ في أوقاتٍ محددةٍ، مع تأمينِ السبلِ المناسبةِ للراحةِ والنقاشِ المفتوحِ حول أيِّ تعديلٍ محتملٍ.

3. `act=0.6271` `token='立ち'`  
   駅で観光客が立ち止まり、僕は急いでスリップインしました。

4. `act=0.6241` `token='▁beruh'`  
   Wenn wir auch nach Kräften bemüht wären, die familiären Verhältnisse sachlich zu analysieren, bliebe dennoch oft unklar, ob die realisierte Kommunikationsstruktur auf tief verwurzelten emotionalen Mustern oder lediglich vorübergehenden externen Einflüssen beruhe.

5. `act=0.6074` `token='姿'`  
   森の中を進んでいると、突然鹿が草の間から姿を現した。

6. `act=0.6052` `token='▁insist'`  
   Mientras el profesor explica las dificultades que enfrentan los estudiantes en una escuela pública del centro de la ciudad, dos adolescentes conversan en voz baja acerca de cómo sus padres siempre les insisten en estudiar más duro para tener un futuro mejor.

7. `act=0.5931` `token='▁집'`  
   이렇게 맛있는 간장게장이 집에 있을 줄은 정말 몰랐어! 아빠가 어머니 생일 선물로 사두셨던 거래서 깜짝 놀랐지.

8. `act=0.5891` `token='▁beruh'`  
   Weil die Regierung den Haushalt vorschob, beruhigte sich die Opposition.

## Candidate 3: feature 7096

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.594`
- validation effect: `+0.394`
- test effect: `+0.215`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.609`

### Top natural activations

1. `act=0.9836` `token='ykke'`  
   Kievariainen lehtiviliö kasvaa metsän pimeässä vyöhykkeessä.

2. `act=0.9832` `token='систем'`  
   В лесу каждый вид птиц занимает своё уникальное место в экосистеме.

3. `act=0.9792` `token='diversidad'`  
   Las especies de árboles nativos, que incluyen tanto ejemplares de hoja caduca como perennes, crecen abundantemente en las zonas húmedas de la región montañosa, donde el clima cálido y las precipitaciones regulares favorecen su desarrollo saludable y la biodiversidad circundante.

4. `act=0.9391` `token='diversidad'`  
   Este sistema ecológico, ubicado a pocos kilómetros de aquí, presenta una biodiversidad notable comparada con las zonas más distantes del bosque.

5. `act=0.9383` `token='diversidad'`  
   La selva amazónica, que abarca una extensa región en varios países de Sudamérica y alberga una biodiversidad única del mundo, enfrenta cada vez más riesgos por la deforestación acelerada y el cambio climático global.

6. `act=0.9262` `token='diversidad'`  
   El río, que discurre por el corazón del bosque, muestra una gran biodiversidad en su orilla oriental.

7. `act=0.9146` `token='▁reserve'`  
   The research team discovered two new species of rare beetles living exclusively in the wetlands near the northern edge of the protected forest reserve.

8. `act=0.9101` `token='diversidad'`  
   Los bosques tropicales albergan mucha biodiversidad.

## Candidate 4: feature 6029

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.603`
- validation effect: `-0.319`
- test effect: `-0.019`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.466`

### Top natural activations

1. `act=0.8239` `token='▁clar'`  
   El aumento significativo en el número de desplazamientos internos durante el último trimestre del año pasado refleja con claridad los impactos sociales derivados de la escalada de conflictos intercomunitarios en varias regiones del país.

2. `act=0.8207` `token='▁clar'`  
   En el documental sobre el campeonato de fútbol femenino se mostró con claridad cómo las jugadoras, sin necesidad de mencionar sus nombres en cada plan, demostraron habilidades excepcionales que hicieron del partido un espectáculo emocionante para todos los aficionados.

3. `act=0.8119` `token='▁clar'`  
   El jefe de proyecto siempre llega temprano para asegurarse de que el equipo esté organizado y listo para comenzar la jornada con claridad de objetivos y fluidez operativa.

4. `act=0.7920` `token='▁clar'`  
   El equipo local vence al visitante con claridad.

5. `act=0.7885` `token='▁clar'`  
   El equipo de fútbol femenino ganó con claridad el campeonato regional.

6. `act=0.7875` `token='▁klar'`  
   Erst der Sprint macht den Sieg klar.

7. `act=0.7850` `token='▁clar'`  
   El equipo ganó el partido con claridad.

8. `act=0.7822` `token='▁clar'`  
   El equipo local ganó el partido con claridad, y sus jugadores celebraron con entusiasmo.

## Candidate 5: feature 6863

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.732`
- validation effect: `+0.371`
- test effect: `-0.252`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.422`

### Top natural activations

1. `act=0.6972` `token='▁dann'`  
   Obwohl ich am liebsten immer alleine arbeite, stelle ich fest, dass manchmal gerade im Projektteam die Ideen am besten zueinanderfinden und sich dann ganz anders weiterentwickeln als geplant.

2. `act=0.6970` `token='▁dann'`  
   Manchmal kann man bei der Arbeit einfach nicht genug tun, um das Tempo mitzugehen, und dann merkt man plötzlich, dass die Zeit verflogen ist, ohne etwas wirklich zu Ende gebracht zu haben.

3. `act=0.6884` `token='▁dann'`  
   Wir haben beschlossen, den Bericht nächste Woche zu prüfen und ihn dann an die Geschäftsleitung weiterzuleiten.

4. `act=0.6758` `token='▁dann'`  
   Ich habe heute Morgen den Brief geschrieben, den ich gestern Abend noch überarbeiten wollte, aber dann wurde es schon zu spät, und ich bin todmüde ins Bett gefallen.

5. `act=0.6704` `token='края'`  
   Спортът е като живота – тренираш усилено и накрая печелиш награда.

6. `act=0.6659` `token='▁afterwards'`  
   I had already finished my homework before dinner yesterday, so I was able to watch the whole movie afterwards.

7. `act=0.6553` `token='▁then'`  
   I'll see you at dinner, then?

8. `act=0.6499` `token='▁dann'`  
   Trotz der Regenwetterbedingungen, die den Tag über die Terrasse nutzbar machten, blieb das Grillfleisch am Abend wunderbar zart und aromatisch, weil wir es bereits am Vormittag mariniert und dann sorgfältig im Ofen bei niedriger Temperatur gegart hatten.

---

# Variable 26: evidentiality

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.195**

## Candidate 1: feature 11375

- selection: `original_trainval_selected`
- train effect: `+0.876`
- validation effect: `+0.028`
- test effect: `-0.743`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `3.848`

### Top natural activations

1. `act=1.1809` `token='▁göre'`  
   Görüşlerine göre, evde tuz yakıt olarak kullanıldığını fark ettiğimizde, yemek yapmayı bıraktıklarını anladık.

2. `act=1.1298` `token='▁göre'`  
   Görüşmemize göre bir sonraki toplantıda sunulan raporda verilerin büyük çoğunluğunun önceki yıllara oranla önemli ölçüde düştüğü belirtilmiş ve bu durumun ekonomik durgunlukla ilişkili olabileceği şeklinde bir yorum yapılmış.

3. `act=1.1298` `token='▁göre'`  
   Görüşmemize göre proje zamanında tamamlanabilir.

4. `act=1.1298` `token='▁göre'`  
   Görüşmemize göre, bu tür iş süreçlerinde aksiliklerin ortaya çıkma ihtimali neredeyse %100'dür çünkü dikkatle planlanmamış iş akışlarında beklenmedik sorunlar oldukça sık rastlanan bir durumdur.

5. `act=1.1298` `token='▁göre'`  
   Görüşmemize göre, yeni sistem pazara çıkış tarihiyle ilgili olasılıklar %70 gibi görünüyor.

6. `act=1.1298` `token='▁göre'`  
   Görüşmemize göre, yeni sistem bu hafta test aşamasına geçebilir.

7. `act=1.0568` `token='▁göre'`  
   Bu raporun içeriğine göre projenin bu aşamasında müdürün doğrudan takibinin olması muhtemelen çok büyük bir risk taşımadan işi yoluna koyacak, çünkü ekibin motivasyonunun düşmesi tehlikesiyle karşı karşıya olduğumuzda sadece planlı faaliyetler değil aynı zamanda kritik karar alma süreçlerinin de hızlandırılması şart.

8. `act=1.0485` `token='▁göre'`  
   Görünenlere göre yeni laboratuvar ölçümleri, önceki hesaplamalardan tahmin edilen değerlerin yaklaşık yüzde otuz oranında farklı olduğunu göstermektedir.

## Candidate 2: feature 9646

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.878`
- validation effect: `+0.087`
- test effect: `-0.713`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `3.535`

### Top natural activations

1. `act=1.8310` `token='▁lokal'`  
   Die Künstlerin spendete ihre neuesten Gemälde der lokalen Galerie für die kommende Ausstellung.

2. `act=1.7739` `token='▁local'`  
   Les touristes qui visitent la Provence aiment généralement passer leur après-midi à flâner dans les petites rues pavées des villages, à déguster un vin local au frais ou à profiter du coucher de soleil sur les collines environnantes.

3. `act=1.7609` `token='▁local'`  
   Dans cette auberge de campagne, le pain frais est toujours accompagné d’un fromage local.

4. `act=1.7465` `token='▁local'`  
   Aunque el estudio concluyó que los consumidores habían preferido productos frescos elaborados localmente, los fabricantes anunciaron planes para exportar su producción a mercados internacionales, según revela un informe publicado esta semana por la Asociación de Alimentación Sostenible.

5. `act=1.7379` `token='▁lokal'`  
   Wenn ein Reisender sich nicht für die lokalen Verkehrsbedingungen interessiert, kann er leicht in die Falle lauter unerwarteter Hindernisse laufen, die für Einheimische selbstverständlich sind und die jedermann behindern können, der nicht genügend aufmerksam den üblichen Routinen folgt.

6. `act=1.7346` `token='▁local'`  
   Ces tableaux de ma grand-mère, si détaillés, reflètent une époque où l'art local était encore vivant dans chaque village.

7. `act=1.7318` `token='▁local'`  
   Le guide les emmène dans le jardin de l’ancienne demeure pour leur montrer les sculptures méconnues du sculpteur local.

8. `act=1.7289` `token='▁local'`  
   C’est à la galerie qu’on a vu cette magnifique exposition d’art local.

## Candidate 3: feature 76

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.872`
- validation effect: `+0.094`
- test effect: `-0.646`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `3.025`

### Top natural activations

1. `act=0.8854` `token='▁по'`  
   В каждом из двадцати домов по улице Мира каждый житель получил одинаковый комплект полезных товаров от местной администрации.

2. `act=0.8721` `token='▁по'`  
   В каждом из трёх финальных матчей чемпионата мира по волейболу хотя бы один из центральных блокирующих игроков обеих сборных продемонстрировал выдающиеся результаты, превратив свои действия в ключевой фактор победы команды.

3. `act=0.8637` `token='▁по'`  
   У каждой из моих бабушек, даже тех, кто уже не выходит из дома, обязательно найдётся по нескольку разнообразных лекарств в аптечке и по одному горячему чаю перед сном.

4. `act=0.8630` `token='▁по'`  
   В каждом доме живёт по-своему дух, свой неповторимый ритм бытия.

5. `act=0.8630` `token='▁по'`  
   В каждом доме живёт по одному ребёнку, который помогает родителям по дому.

6. `act=0.8607` `token='▁göre'`  
   Bulunduğu ortamın pH seviyesine göre rengi değişen maddelere göstergeler denir.

7. `act=0.8528` `token='▁по'`  
   Каждый из нас взял по одному напитку и расставил их на столе так, чтобы все гости могли легко достать себе что-нибудь.

8. `act=0.8503` `token='▁по'`  
   В каждом из этих домов живёт по пять сестёр, и каждая из них помогает содержать всех вместе.

## Candidate 4: feature 6900

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.880`
- validation effect: `+0.761`
- test effect: `-0.072`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `3.017`

### Top natural activations

1. `act=1.1460` `token='miş'`  
   Eğer daha erken kalksaydım, işe yakında bir kahve alıp sakin sakin gitmiş olurum.

2. `act=1.1374` `token='miş'`  
   Gece yarısı onlar eve dönmüşken, bu sefer araba onun değilmiş.

3. `act=1.1253` `token='miş'`  
   Bugün en sevdiğim filmden bir sahneyi düşünerek klasik komedyeyi izlememişim, çünkü geçen hafta sık sık onu izlediğimden dolayı yeni bir sinema filmi izlemek istiyordum.

4. `act=1.1214` `token='miş'`  
   Adaylarımı memnun edemeyecek pozisyonlarla ilgilenmiş olsam da, onların beklentilerini göz önünde bulundurarak daha etkili bir staj programı geliştirmelerini sağlamış oldum.

5. `act=1.1164` `token='miş'`  
   Birkaç yıldır çalışmakta olduğum ofisimdeki masa artık benimkisi değilmiş gibi hissediyorum, çünkü yeni işe başladığım şirket daha ergonomik bir çalışma ortamı için tüm sandalyeleri ve masaları değiştirmeyi planlıyor.

6. `act=1.1152` `token='miş'`  
   Bu ağaçlar daha önce burada değilmiş.

7. `act=1.1148` `token='miş'`  
   Kuzenim evde değilmiş gibi duydum, çünkü çocuklarımdan biri onu sokakta Esra hanım olarak tanıştırmış.

8. `act=1.1048` `token='miş'`  
   Ah be ne mutlu di miydi ki sabah uyandığımda bu deneyi başarmış haliyle televizyonda bir haber olarak izlemiş olmuştum.

## Candidate 5: feature 10641

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.876`
- validation effect: `+0.714`
- test effect: `+0.201`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.577`

### Top natural activations

1. `act=0.8621` `token='今'`  
   駅で家族に会ったとき、今週の予定を話しました。

2. `act=0.8424` `token='今'`  
   東京駅で新幹線の最終電車を逃したとき、友達に「次回はもっと早く行かなきゃね」と笑いながら言って、今度は自分でもっと時間に余裕を持とうと決意した。

3. `act=0.8250` `token='今'`  
   その旅行社のカウンターで今すぐ手配できる旅行プランなら、この週末にでも出発して、来週の月曜日には帰ってくる予定になっているので、今のうちにしっかり話をつけておいた方がいいよ。

4. `act=0.8164` `token='今'`  
   この会社の新規オフィスは隣町に移転したため、今週末に従業員全員が現地へ移動し、新しい職場で業務を開始する予定だ。

5. `act=0.8122` `token='今'`  
   その資料はここで説明されていることが理解できないまま次の場所に移ったために、今度はあの遠く離れたホールの隣にある学習コーナーで同じ内容についてもっと詳しい説明を聞くことにしました。

6. `act=0.8112` `token='今'`  
   母に電話で、今週末に私たち家族が東京ドームの近くのホテルに泊まることになったので、お父さんと妹を連れてその辺りを一緒に散歩してみないかと誘ってみたいと思っているんだけど、どう思う？

7. `act=0.8076` `token='今'`  
   それにしても、水墨画は日本の文化を象徴する芸術として、今もなお多くの人々に親しまれている。

8. `act=0.8040` `token='今'`  
   東京を出発して、新幹線で長野に向かっている途中で、窓の外に雪がちらつく様子を見ながら、あの有名な音楽ホールでコンサートを聴けることを今から楽しみにしていました。

---

# Variable 27: mirativity_stance_and_affect_marking

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 1887

- selection: `original_trainval_selected`
- train effect: `+0.975`
- validation effect: `+0.855`
- test effect: `+0.952`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.395`

### Top natural activations

1. `act=2.9499` `token='、'`  
   毎朝コーヒーを淹れながら、テレビで気象予報を見てから出かけようと思っているんですけど、今日は体調がよくなくて、ちょっとお風呂にゆっくり入ってからにするつもりです。

2. `act=2.8529` `token='、'`  
   お父さんが朝食を食べ終わったあとの皿やコップは、ちょっと手伝っていただけますか。できれば今のうちにお洗濯機に回してしまいたいんですけど、ほかにも何やらやらなければならないことがあって。

3. `act=2.8119` `token='。'`  
   この夏休みに、友達と京都へ行って、古い神社や仏閣を巡る予定だったんですけど、天気が悪くて計画がずれてしまいました。

4. `act=2.7990` `token='。'`  
   薬が効いたのを驚いて、母は笑いました。

5. `act=2.7979` `token='。'`  
   こんなに古い芸術作品が完璧な状態で保存されていたなんて、驚きですね。

6. `act=2.7918` `token='。'`  
   朝ごはんに納豆ご飯を食べるのと、サラダを食べるのでは、味や栄養バランスが大きく違うので、今日もどちらか一方にするつもりでしたが、結局時間がないため、目玉焼きだけを急いで食べてきました。

7. `act=2.7882` `token='。'`  
   最近、体の具合がよくなくて、薬を飲んだあとで必ず休まないと気が入らなくて、仕事にも支障が出たりするようになりました。

8. `act=2.7725` `token='。'`  
   庭で花を見ていたら、カモミールが自然に生えていて驚きました。

## Candidate 2: feature 6043

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.961`
- validation effect: `-0.986`
- test effect: `-0.920`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.058`

### Top natural activations

1. `act=1.3734` `token='▁我們'`  
   我們馬上啟程去機場。

2. `act=1.3734` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

3. `act=1.3734` `token='▁我們'`  
   我們明天早上七點出發。

4. `act=1.2846` `token='▁Fr'`  
   Früchte und Gemüse tragen zur gesunden Ernährung bei.

5. `act=1.2843` `token='▁Kongre'`  
   Kongre başkanı, üyeleri protesto etmekten vazgeçirecek bir karar aldı.

6. `act=1.2843` `token='▁Kongre'`  
   Kongre, yeni yasal düzenlemeleri görüşmek üzere toplandı.

7. `act=1.2843` `token='▁Kongre'`  
   Kongrede konu, sert eleştirilere maruz kaldı.

8. `act=1.2843` `token='▁Kongre'`  
   Kongre, yasal prosedürlerin çoğunu tekrarlayan ancak konuyu açıklığa kavuşturan bir tartışmayla oylamaya sunmayı kararlaştırdı.

## Candidate 3: feature 8362

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.962`
- validation effect: `-0.987`
- test effect: `-0.920`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.056`

### Top natural activations

1. `act=2.3715` `token='▁Sana'`  
   Sana Ankara'da bir süre önce açılan o küçük resim galerisinden bir yağlı boya almamı önermiştim ya, ondan biraz sonra sokağın karşısındaki kafede tanıştığımız eski profesörümüz de bahseden diğeri gibi bir yapıtı olduğunu söylemişti.

2. `act=2.3715` `token='▁Sana'`  
   Sana akşam yemeğinde pilav yapacağım.

3. `act=2.3715` `token='▁Sana'`  
   Sana çok güzel bir hediye getirdim.

4. `act=2.3715` `token='▁Sana'`  
   Sana yardım etmek isterdim ama işim başlamak üzereydi.

5. `act=2.3715` `token='▁Sana'`  
   Sana da bir fincan çay getirsem mi?

6. `act=2.3715` `token='▁Sana'`  
   Sana yardımcı olmaya çalıştım ama neye yarar bilmiyorum.

7. `act=2.3715` `token='▁Sana'`  
   Sana yardım edeyim mi?

8. `act=2.3636` `token='▁Сло'`  
   Слой за слоем, словно россыпь таинственных страниц, мы покидаем старую кухню, где висел на стене бабушкин подвешенный свитер, и мчится вперёд – в будущее, где даже её любимые пирожки обретают новый вкус.

## Candidate 4: feature 785

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.962`
- validation effect: `-0.985`
- test effect: `-0.920`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.056`

### Top natural activations

1. `act=2.0995` `token='▁Olet'`  
   Oletko ymmärtänyt, että tämän monimutkaisen perheverkon sisällä jotkut henkilöt, kuten esimerkiksi aviopuoliso tai puolison veli, voivat olla vastuualueellisesti osa päätöksentekovaltaistoa suhteessa muihin lähisukulaisiin?

2. `act=2.0995` `token='▁Olet'`  
   Oletko varma, että laitit naisen lemmikkikoiran lemmikkieläimensä ruokakotelo kaapin yläpuolelle?

3. `act=2.0995` `token='▁Olet'`  
   Oletko nälkäinen?

4. `act=2.0995` `token='▁Olet'`  
   Oletko sairaana?

5. `act=2.0958` `token='▁Debe'`  
   Debes apagar las luces antes de salir, aunque parezca que ya se fue la electricidad.

6. `act=2.0958` `token='▁Debe'`  
   Debes apagar las luces antes de salir para ahorrar energía.

7. `act=2.0958` `token='▁Debe'`  
   Debes apagar la luz antes de salir de la habitación.

8. `act=2.0958` `token='▁Debe'`  
   Debes cuidar que las obras de arte expuestas en el museo permanezcan protegidas contra la humedad y la contaminación del aire.

## Candidate 5: feature 9535

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.962`
- validation effect: `-0.987`
- test effect: `-0.920`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.056`

### Top natural activations

1. `act=2.5575` `token='▁Mey'`  
   Meydanın karşısında açılan yeni kafenin çatısında metal bir tabela göründü.

2. `act=2.5575` `token='▁Mey'`  
   Meyve sepetini alırken parkta karşılaşmıştık.

3. `act=2.4629` `token='▁Hazır'`  
   Hazırlanan projeyi öğretmenler değerlendirdi.

4. `act=2.4593` `token='▁Five'`  
   Five conservation teams surveyed twenty wetland sites along the coastal reserve last week.

5. `act=2.4550` `token='▁Cinc'`  
   Cinco manifestantes arrestados durante la protesta en la capital fueron liberados bajo fianza.

6. `act=2.4550` `token='▁Cinc'`  
   Cinco estudiantes entregaron tres ensayos cada uno para la clase de literatura.

7. `act=2.4550` `token='▁Cinc'`  
   Cinco amigos ayudaron a cada uno de los ancianos a cruzar la calle.

8. `act=2.4545` `token='▁Hmm'`  
   Hmm, bu toplantıda bu kadar hızlı karar vermenin beklenmedik bir sonucu olur muydu?

---

# Variable 28: negation_and_polarity_structure

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.960**

## Candidate 1: feature 4382

- selection: `original_trainval_selected`
- train effect: `+0.604`
- validation effect: `+0.282`
- test effect: `+0.386`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.149`

### Top natural activations

1. `act=1.0896` `token='▁entre'`  
   Chaque habitant de l’immeuble reçoit deux boîtes de conserve par mois, mais quand on les ouvre, il se révèle que toutes contiennent soit des haricots rouges, soit des lentilles, sans variété apportée entre les différentes unités livrées.

2. `act=1.0760` `token='▁entre'`  
   Aunque yo haya participado en la marcha, nadie me reconoció entre la multitud.

3. `act=1.0617` `token='▁entre'`  
   Cuando mi hermana menor fue a visitar a su tía abuela, encontró una antigua caja de fotos debajo de la cama que nadie había abierto desde hace años, y entre todas esas imágenes desgastadas, reconoció a nuestro tío materno cuando tenía apenas cinco o seis años, jugando junto a mis primos en el jardín trasero del viejo rancho familiar.

4. `act=1.0592` `token='▁zwischen'`  
   Als sie endlich die Tür öffnete, stand er immer noch reglos da, als hätte er Angst, die Stille zu durchbrechen, die zwischen ihnen entstanden war, seit sie nicht mehr wusste, was sie sagen sollte.

5. `act=1.0547` `token='▁zwischen'`  
   An der U-Bahn-Haltestelle stieß ich auf ein älteres Ehepaar aus Schweden, das den deutschen Sprachunterschieden wegen besonders langsam voranging und zwischendurch gerne Halt suchte, um sich die fremden Straßennamen und die Schilder am Bahnhof genauer anzusehen.

6. `act=1.0498` `token='entre'`  
   Ce matin-là, en ouvrant le journal, il lut avec étonnement l'entrefilet qui parlait du nouveau projet de loi sur les transports en commun voté par l’assemblée régionale.

7. `act=1.0484` `token='▁entre'`  
   Vimos cómo el río cruzaba el valle antes de perderse entre los árboles del bosque cercano.

8. `act=1.0405` `token='▁zwischen'`  
   In großen Galerien wie der Berliner Volksbühne ist es üblich, dass Künstler an mehreren Projekten gleichzeitig arbeiten und zwischen Theater, Ausstellungen und Festivals wechseln, als wären diese Formen nur verschiedene Facetten derselben kreativen Wirklichkeit.

## Candidate 2: feature 13008

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.614`
- validation effect: `+0.349`
- test effect: `+0.485`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.697`

### Top natural activations

1. `act=0.7662` `token='▁forgotten'`  
   After booking our tickets online and printing out the boarding passes, we realized we had forgotten to pack the passports we needed to show at security before boarding the flight.

2. `act=0.7598` `token='▁to'`  
   A group of travelers said they were disappointed when their guide forgot to book the airport transfers.

3. `act=0.7576` `token='▁to'`  
   They scheduled the meeting yesterday but forgot to send the email.

4. `act=0.7560` `token='▁forgotten'`  
   She was mixing the batter when she realized she had forgotten the baking powder.

5. `act=0.7511` `token='▁forgotten'`  
   After booking the flight, I realized I had forgotten my passport.

6. `act=0.7494` `token='▁to'`  
   After eating breakfast and checking my messages, I realized I had forgotten to water the plants, so I quickly ran outside before they turned completely dry.

7. `act=0.7491` `token='▁to'`  
   The cake burned because I forgot to turn down the heat.

8. `act=0.7449` `token='▁to'`  
   I had just finished making the apple pie when I realized I'd forgotten to set the oven timer, so it ended up a bit too browned around the edges.

## Candidate 3: feature 12169

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.566`
- validation effect: `-0.152`
- test effect: `-0.409`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.655`

### Top natural activations

1. `act=1.3821` `token='▁veces'`  
   Aunque ya era tarde y había decidido que ese día no saldría de casa, al final terminé cogiendo el coche, conduciendo hasta la estación de tren y comprando un billete para salir de viaje, porque a veces es necesario moverse incluso cuando todo indica que lo mejor sería quedarse quieto.

2. `act=1.3004` `token='▁veces'`  
   Tu hablas de tecnología como si fuera algo sencillo, pero a veces me siento perdido.

3. `act=1.2625` `token='х'`  
   У взрослого человека руки и ноги считаются частью тела, но в некоторых культурах украшения на них могут передаваться по наследству.

4. `act=1.2561` `token='▁vezes'`  
   Viajar sozinho tem suas vantagens, mas às vezes um(a) companheiro(a) faz a viagem ser ainda melhor.

5. `act=1.2560` `token='▁veces'`  
   Al presentar el informe sobre las dinámicas familiares en diferentes culturas, ella les recordó a los asistentes que el rol del padrastro en la sociedad africana se valora tanto como el del padre biológico, y que incluso a veces él recibe más respeto por su disposición protectora y generosa.

6. `act=1.2478` `token='▁veces'`  
   Mientras el chófer revisaba el mapa para elegir el mejor camino y ella le indicaba con claridad hacia dónde debían ir, él comentó que a veces los trayectos más largos terminan siendo los más entretenidos si se comparten con alguien interesado en la historia de cada lugar por el que pasaban.

7. `act=1.2303` `token='▁veces'`  
   Muchas personas prefieren que se les reconozca por sus logros, pero a veces las circunstancias lo deciden todo.

8. `act=1.2268` `token='▁veces'`  
   Desde que me mudé a la ciudad, siempre he notado cómo las conversaciones cambian de tono dependiendo de la hora del día, y aunque a veces prefiero quedarme en casa leyendo un buen libro, también disfruto encontrarme con amigos que, al igual que yo, han dejado atrás la monotonía del trabajo para compartir una cerveza o simplemente charlar sobre el fin de semana que está por llegar.

## Candidate 4: feature 16131

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.563`
- validation effect: `+0.410`
- test effect: `+0.499`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.651`

### Top natural activations

1. `act=0.8722` `token='少し'`  
   山田さん、タクシーを呼んでいただけますか。少し時間がないのでお願いします。

2. `act=0.8434` `token='少し'`  
   窓を開けてください。少し涼しくなりました。

3. `act=0.8389` `token='ちょっと'`  
   このたび引っ越してきて、隣の家はとても静かで落ち着いていて、ちょっと遠回りになってしまうけれど買い物にも便利な場所に住んでいるんですけど、以前の賃貸アパートのように頻繁にお隣さんと顔を合わせるようなことはあまりなくなりました。

4. `act=0.8326` `token='ちょっと'`  
   お父さんが朝食を食べ終わったあとの皿やコップは、ちょっと手伝っていただけますか。できれば今のうちにお洗濯機に回してしまいたいんですけど、ほかにも何やらやらなければならないことがあって。

5. `act=0.8323` `token='ちょっと'`  
   お風呂に入る前にお母さん、ちょっと病院の予約の話をしているんだけど、明日の午後に受診したいと思ってるから、今週中に薬を飲むのを忘れずにねとお願いしていたんです。

6. `act=0.8299` `token='ちょっと'`  
   でも、最近の彼は昔ほど素直じゃなくて、ちょっと困ってるんだよね。

7. `act=0.8299` `token='少し'`  
   そのプロジェクトの資料をすべてチェックし終えてから、なぜ社長が最初に社員の意見を聞かずに決定したのか、少し疑問に思っていた。

8. `act=0.8207` `token='ちょっと'`  
   お茶をいれていただけますか。ちょっと疲れました。

## Candidate 5: feature 3522

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.568`
- validation effect: `-0.377`
- test effect: `-0.398`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.514`

### Top natural activations

1. `act=1.8407` `token='सर'`  
   यात्रा करते समय पशु या मनुष्य को अक्सर विशेष रूप से ध्यान दिया जाता है।

2. `act=1.7856` `token='▁spesso'`  
   In molti ambienti lavorativi, capita spesso che si rifiuti di partecipare ai meeting se non si è preparati, soprattutto quando si tratta di discutere progetti complessi con clienti importanti.

3. `act=1.7851` `token='▁spesso'`  
   In molte situazioni accademiche, capita spesso di dover riscrivere un testo per renderlo più chiaro e coerente, ma anche quando i tempi sono stretti, il soggetto può essere omesso senza ambiguità se il contesto lo permette.

4. `act=1.7575` `token='सर'`  
   यात्रा करते समय विमान अक्सर बादलों के माध्यम से गुजरता है।

5. `act=1.7331` `token='सर'`  
   शिक्षा के बारे में बहस करते समय वह अक्सर अपने पिता की बातों पर ध्यान नहीं देती।

6. `act=1.7097` `token='सर'`  
   रोगियों को अक्सर अपनी मानसिक स्थिति पर ध्यान देने और एक-दूसरे के साथ संवाद करने की आवश्यकता होती है।

7. `act=1.6942` `token='▁spesso'`  
   Quando si parla di cucina, capita spesso che mentre uno ti mostra con orgoglio il suo nuovo fornello a induzione, l’altro commenta sottovoce che lui invece preferisce sempre il vecchio metodo con la fiamma diretta, e quel contrasto tra modernità e tradizione riesce quasi sempre a scatenare una bella discussione tra amici.

8. `act=1.6927` `token='▁often'`  
   In dietary studies, it's often noted that the absence of a single nutrient doesn't necessarily mean poor nutrition if other essential components are present in adequate amounts.

---

# Variable 29: quantifier_scope_and_distributivity

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 8551

- selection: `original_trainval_selected`
- train effect: `+0.700`
- validation effect: `+0.475`
- test effect: `+0.313`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.273`

### Top natural activations

1. `act=1.5246` `token='▁पक्ष'`  
   दो पक्षियाँ पेड़ पर बैठी हैं।

2. `act=1.4547` `token='▁छात्र'`  
   हमारी कक्षा में दस छात्र हैं।

3. `act=1.4362` `token='▁पक्ष'`  
   बच्चा मन ही मन चार पक्षियों के पीछे दौड़ रहा था।

4. `act=1.4143` `token='▁مدارس'`  
   في المدينة ثلاث مدارس جديدة.

5. `act=1.4117` `token='▁छात्र'`  
   कक्षा में दो छात्र चले गए।

6. `act=1.4106` `token='▁hasta'`  
   Yeni açılan eczane binasında çalışan doktor, üç hasta ile beraber güvenli bir şekilde maskesiz konuşabildi.

7. `act=1.4102` `token='▁ana'`  
   Yeni yasada üç ana değişiklik yapıldı.

8. `act=1.3959` `token='▁kişi'`  
   Deney grubunda sekiz kişi, sağlıklı beslenme programına dahil edildi.

## Candidate 2: feature 3720

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.650`
- validation effect: `+0.078`
- test effect: `-0.116`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `7`
- specificity ratio: `0.714`

### Top natural activations

1. `act=0.5062` `token='▁Kasım'`  
   Kasımın sonlarına doğru grip kapmamış olsaydım doktora gitmemi sen istemiştin ama aslında kendim de çayımı içmem için babama izin vermemiştim çünkü çok fazla şeker koyduğunu biliyordum.

2. `act=0.5062` `token='▁Kasım'`  
   Kasımpaşa'nın bu maçta kazanma şansı oldukça yüksek gibi görünüyor ama emin olmak güç.

3. `act=0.5062` `token='▁Kasım'`  
   Kasımda kurulan mecliste ilk adımın atılmasıyla kabine tartışmaları başladı.

4. `act=0.5062` `token='▁Kasım'`  
   Kasım ayında yapılan genetik testlerin sonuçlarına göre hastalığın bu türü insanların bağışıklık sistemini ciddi şekilde zayıflatan ve uzun süreli tedavi gerektiren bir mutasyonla ilişkili olduğu ortaya çıkmıştır.

5. `act=0.5062` `token='▁Kasım'`  
   Kasımın sonunda başlayan bu grip beni hem yorgun hissettirdi hem de dengemden kaydırdı.

6. `act=0.5051` `token='▁서울'`  
   서울에서 열린 정책간담회에서 장관은 "지역균형발전을 위해서는 공정한 자원배분이 필수적이다"라고 강조하며, 관련 예산 증액을 촉구했다.

7. `act=0.5051` `token='▁서울'`  
   서울역 앞에서는 어머니와 함께 있는 딸이 여행 짐을 정리하고 있었다.

8. `act=0.5051` `token='▁서울'`  
   서울의 작은 식당에서 잡채를 먹으며 주변을 둘러보니, 오래된 건물과 현대적인 모습이 공존하는 골목길의 분위기와 마찬가지로 음식도 전통과 현대가 혼합된 듯해 눈에 띄었다.

## Candidate 3: feature 12588

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.727`
- validation effect: `+0.279`
- test effect: `+0.376`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `8`
- specificity ratio: `0.774`

### Top natural activations

1. `act=0.9813` `token='▁نعم'`  
   نعم، سيعقد الامتحان بعد الغد الساعة الثانية ظهرًا في قاعة الطلاب الجديدة.

2. `act=0.9813` `token='▁نعم'`  
   نعم، أدرك أنه بعد فترة الصوم الطويلة التي مرَّ بها الجسم وكانوا يعانون من سوء تغذية خطير، فقد تحسنت قدرتهم على التحمل بشكل ملحوظ.

3. `act=0.9749` `token='▁الطائ'`  
   الطائرة أقلعت من المطار بسلاسة دون أي تأخير ملحوظ.

4. `act=0.9656` `token='▁الخط'`  
   الخطة التي قدمها المهندس لم تكن مبنية على التقديرات الأولية للجنة الفنية.

5. `act=0.9654` `token='▁عادت'`  
   عادت الأم وأغلقت الباب وضعت الكوب على الطاولة.

6. `act=0.9654` `token='▁عادت'`  
   عادتُ إلى المنزل فوجدتُ والدتي تطبخُ طبقاً مألوفاً.

7. `act=0.9612` `token='▁گری'`  
   گری لہریں چل رہی تھیں اور سورج میں سب کچھ فضا میں تھا۔

8. `act=0.9531` `token='▁سمع'`  
   سمعت عن فتاة ثلاث ذهبت للعمل في الشركة الجديدة.

## Candidate 4: feature 14198

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.704`
- validation effect: `+0.519`
- test effect: `+0.032`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `9`
- specificity ratio: `0.742`

### Top natural activations

1. `act=0.6388` `token='▁Looking'`  
   Looking out the window right now, you can see that this little park just down the street has become really popular lately, while the bigger one over there on the other side of town seems almost empty these days.

2. `act=0.6388` `token='▁Looking'`  
   Looking around the conference room where the team presentation will start in ten minutes, I quickly grab the laptop I brought yesterday and check once more if all the notes we prepared last week are on the shared drive so everyone can access them now.

3. `act=0.6388` `token='▁Looking'`  
   Looking at the lab results here versus those from last week there, the differences seem quite significant.

4. `act=0.6388` `token='▁Looking'`  
   Looking back on that summer performance at the outdoor theater, I realize how much more vividly she remembered the moment I had just finished reciting the monologue under the strings of fairy lights than I did myself.

5. `act=0.6388` `token='▁Looking'`  
   Looking back, the mayor’s controversial remarks during the press conference still spark heated debates across town.

6. `act=0.6388` `token='▁Looking'`  
   Looking back on how I've managed my time this past month, I've really noticed that I've become much more efficient at balancing work and personal commitments.

7. `act=0.6388` `token='▁Looking'`  
   Looking around the gallery, I noticed that while most people were drawn to the bright, colorful paintings near the entrance, she stood captivated by the quiet, abstract piece in the farthest corner.

8. `act=0.6388` `token='▁Looking'`  
   Looking back on that early prototype we built, I can’t help but notice how much simpler everything seemed then compared to the complex systems we're dealing with now.

## Candidate 5: feature 14976

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.679`
- validation effect: `+0.280`
- test effect: `+0.334`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `9`
- specificity ratio: `0.740`

### Top natural activations

1. `act=0.6401` `token='▁نعم'`  
   نعم، أدرك أنه بعد فترة الصوم الطويلة التي مرَّ بها الجسم وكانوا يعانون من سوء تغذية خطير، فقد تحسنت قدرتهم على التحمل بشكل ملحوظ.

2. `act=0.6401` `token='▁نعم'`  
   نعم، سيعقد الامتحان بعد الغد الساعة الثانية ظهرًا في قاعة الطلاب الجديدة.

3. `act=0.6099` `token='▁Pourtant'`  
   Pourtant, la tarte aux pommes de mamie est bien plus réconfortante que ces plats sophistiqués du chef étoilé.

4. `act=0.6099` `token='▁Pourtant'`  
   Pourtant, il préfère peindre des paysages de son enfance plutôt que des rues modernes.

5. `act=0.6099` `token='▁Pourtant'`  
   Pourtant, l'expérience confirme que la théorie est souvent mise à l'épreuve.

6. `act=0.6099` `token='▁Pourtant'`  
   Pourtant, c’est bien ici qu’on aperçoit le mieux la vue sur les collines environnantes.

7. `act=0.6088` `token='▁Usko'`  
   Uskon, että kielitaito paranee parhaiten, kun opiskelija mukailee paikallisen puhetapaiskun erilaisia ilmentymiä.

8. `act=0.6015` `token='▁Five'`  
   Five conservation teams surveyed twenty wetland sites along the coastal reserve last week.

---

# Variable 30: conditional_and_counterfactual_marking

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.936**

## Candidate 1: feature 15951

- selection: `original_trainval_selected`
- train effect: `+0.718`
- validation effect: `+0.179`
- test effect: `+0.304`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.875`

### Top natural activations

1. `act=0.6757` `token='▁be'`  
   It might well be that the researchers have already accounted for atmospheric interference in their model, but given how rapidly conditions change here, I wouldn't be surprised if they double-checked their readings just to be safe.

2. `act=0.6651` `token='hésit'`  
   Il ne faut pas hésiter à demander de l’aide si la situation le nécessite vraiment.

3. `act=0.6242` `token='▁mir'`  
   Wenn die Firma eine flexible Arbeitszeit einrichten würde, könnte ich mir besser einen Termin im Jugendzentrum freinehmen.

4. `act=0.6230` `token='▁see'`  
   Looking around the gallery, you can see that the artist painted the flowers right there near the window, while the trees in the background seem to stretch all the way here to the edge of the canvas.

5. `act=0.6181` `token='▁have'`  
   The player *could have scored* if better positioned.

6. `act=0.6073` `token='▁find'`  
   A visitor can find helpful information at the museum's entrance.

7. `act=0.6053` `token='▁have'`  
   I wouldn’t have guessed you weren’t coming over for dinner tonight.

8. `act=0.6042` `token='▁look'`  
   I wonder if you could look over this report before the meeting tomorrow.

## Candidate 2: feature 6546

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.826`
- validation effect: `+0.100`
- test effect: `-0.124`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.864`

### Top natural activations

1. `act=1.6272` `token='▁aurait'`  
   Si tu avais parlé plus tôt avec ton responsable, on aurait pu éviter ce malentendu.

2. `act=1.6250` `token='▁aurait'`  
   Si tu avais été là, on aurait pu éviter toute cette confusion.

3. `act=1.6247` `token='▁aurait'`  
   Si vous aviez rempli le formulaire, on aurait pu accélérer la procédure.

4. `act=1.5990` `token='▁aurait'`  
   Si tu m'avais demandé mon avis avant de décider, on aurait pu en discuter calmement.

5. `act=1.5978` `token='▁would'`  
   If the algorithm fails to converge, we would have to revise the model's assumptions.

6. `act=1.5726` `token='▁aurait'`  
   Si tu étais venu plus tôt, on aurait pu en discuter avant.

7. `act=1.5726` `token='▁aurait'`  
   Si tu étais venu plus tôt, on aurait pu regarder ce film de famille ensemble, comme avant.

8. `act=1.5694` `token='▁aurait'`  
   Si tu avais apporté ton appareil photo, on aurait pu prendre des photos ensemble.

## Candidate 3: feature 10407

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.786`
- validation effect: `+0.141`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.789`

### Top natural activations

1. `act=1.2829` `token='▁serait'`  
   Puisque tu as mal à la gorge depuis plusieurs jours et que les siropes ne semblent plus faire effet, il serait peut-être temps de consulter un médecin pour qu’il puisse t’examiner et te prescrire quelque chose de plus efficace.

2. `act=1.2810` `token='▁serait'`  
   Il me serait difficile de voyager seul dans ce pays sans connaître la langue locale.

3. `act=1.2618` `token='▁serait'`  
   Pour mieux comprendre l’écosystème local, il serait utile de recueillir des données sur la qualité de l’eau.

4. `act=1.2541` `token='▁serait'`  
   Il serait bien que tu me laisses une minute pour réfléchir à tout ça.

5. `act=1.2541` `token='▁serait'`  
   Il serait bien de laisser les enfants explorer un peu plus loin dans le bois, à condition qu’on puisse entendre leur voix et qu’ils ne s’aventurent pas trop près du ruisseau.

6. `act=1.2541` `token='▁serait'`  
   Il serait bien que nous trouvions un moment pour en parler tranquillement.

7. `act=1.2541` `token='▁serait'`  
   Il serait utile de consulter les résultats avant la prochaine séance.

8. `act=1.2541` `token='▁serait'`  
   Il serait bien que tu ranges un peu ta chambre avant qu'on parte.

## Candidate 4: feature 15938

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.859`
- validation effect: `+0.499`
- test effect: `-0.114`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.701`

### Top natural activations

1. `act=1.2942` `token='▁might'`  
   Had the team trained more consistently during the season, they might have secured a spot in the finals.

2. `act=1.2910` `token='▁might'`  
   Had the team trained more diligently, they might have won the championship.

3. `act=1.2887` `token='▁might'`  
   Had the team trained harder, they might have won the championship.

4. `act=1.2887` `token='▁might'`  
   Had the team trained harder, they might have won the regional championship last weekend.

5. `act=1.2486` `token='▁might'`  
   I heard the clinic next door is hiring part-time nurses. You might want to call them if you're looking for something flexible.

6. `act=1.2319` `token='▁might'`  
   Had the museum hosted the exhibition last year, it might have drawn a more diverse audience.

7. `act=1.2123` `token='▁might'`  
   Had the coach called the timeout, we might have won the game.

8. `act=1.2086` `token='▁might'`  
   Based on the team's performance, they might win the tournament.

## Candidate 5: feature 11810

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.717`
- validation effect: `+0.141`
- test effect: `+0.210`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.688`

### Top natural activations

1. `act=1.0888` `token='aurais'`  
   Si tu avais fait ce test plus tôt, tu aurais pu commencer le traitement dès maintenant.

2. `act=1.0501` `token='avais'`  
   Je me suis levé en retard parce que je n'avais pas bien dormi la veille au soir.

3. `act=1.0484` `token='aurais'`  
   Si tu avais suivi mon conseil, tu n’aurais pas perdu ton temps à chercher ailleurs.

4. `act=1.0460` `token='▁be'`  
   If I had taken that summer course back then, I probably wouldn't be struggling with the requirements now.

5. `act=1.0369` `token='aurais'`  
   Si tu avais été là hier soir, tu aurais aimé la surprise qu’on lui avait préparée.

6. `act=1.0307` `token='aurait'`  
   Si tu avais mis le couvert plus tôt, on n'aurait pas eu à manger debout dans la cuisine.

7. `act=1.0265` `token='▁be'`  
   If I hadn’t missed that connecting flight, I’d probably be home by now.

8. `act=1.0241` `token='aurais'`  
   Je ne vois vraiment pas pourquoi on ne m’a pas dit plus tôt que je n’aurais pas dû avaler tout ce médicament, car je ne me sens absolument pas mieux depuis que j’en prends une dose chaque fois que j’ai mal.

---

# Variable 31: subordination_and_embedding

- Original SAE evidence tier: **A**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.673**

## Candidate 1: feature 7643

- selection: `original_trainval_selected`
- train effect: `+0.927`
- validation effect: `+0.911`
- test effect: `+0.649`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.974`

### Top natural activations

1. `act=1.3762` `token='▁o'`  
   Quando cheguei ao teatro, o espetáculo já tinha começado e sentei-me na primeira fileira para não perder nenhum detalhe da apresentação do grupo local de dança contemporânea.

2. `act=1.3643` `token='▁el'`  
   Después de que el jugador marcó el gol decisivo, el entrenador celebró con su equipo.

3. `act=1.3630` `token='▁las'`  
   Desde que el muralista inició su serie de obras sobre la tradición indígena en la fachada del centro cultural, las representaciones visuales reflejan constantemente la evolución de sus técnicas y su compromiso con la preservación de los símbolos ancestrales.

4. `act=1.3565` `token='▁el'`  
   Cuando le preguntaron por qué se retiró del torneo de tenis, el jugador explicó que había decidido darle prioridad a su recuperación tras la lesión que sufrió en el último partido del campeonato anterior.

5. `act=1.3547` `token='▁le'`  
   Lors du dernier tournoi de tennis local où plusieurs jeunes joueurs passionnés et courageux se sont affairés à démontrer leurs compétences devant une foule enthousiaste et chaleureuse, le match le plus intense et serré a finalement opposé les deux champions en herbe issus d’associations sportives différentes mais tout aussi motivés par leur rêve commun de réussite.

6. `act=1.3464` `token='▁la'`  
   Según el reportero que cubrió la exposición, la obra ganadora fue muy aplaudida por el público presente.

7. `act=1.3419` `token='▁el'`  
   Desde la perspectiva del crítico que recorrió las salas del museo, el reciente restablecimiento de las obras del siglo XIX revela una sensibilidad distinta a la del comisario original, quien había organizado la exposición bajo un enfoque cronológico estricto.

8. `act=1.3365` `token='▁le'`  
   Lorsque j’ai retrouvé mes amis pour déjeuner à l’extérieur, le soleil brillait doucement, la terrasse était pleine de rires et de conversations animées, et tout semblait si naturel après une semaine de travail intense.

## Candidate 2: feature 11461

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.914`
- validation effect: `+0.963`
- test effect: `-0.588`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.473`

### Top natural activations

1. `act=1.8117` `token='▁that'`  
   I heard on the radio that the river levels have risen due to heavy rainfall overnight.

2. `act=1.7961` `token='▁qu'`  
   J'ai entendu dire qu'elle était malade.

3. `act=1.7961` `token='▁qu'`  
   J'ai entendu dire qu'elle avait changé d'avis après avoir discuté avec son meilleur ami.

4. `act=1.7894` `token='▁that'`  
   I heard on the radio this morning that the train service to Manchester will be delayed again tomorrow.

5. `act=1.7516` `token='▁that'`  
   I read somewhere that quantum computing might revolutionize data encryption methods in the near future.

6. `act=1.7387` `token='▁qu'`  
   J’ai entendu dire qu’on servirait du gâteau au dîner.

7. `act=1.7173` `token='▁qu'`  
   Il faut que tu essaies ce nouveau club de golf, j’ai entendu dire qu’il est génial pour les débutants.

8. `act=1.7128` `token='▁that'`  
   I heard somewhere that train tickets sold out fast this season.

## Candidate 3: feature 2726

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.944`
- validation effect: `+0.982`
- test effect: `-0.058`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.415`

### Top natural activations

1. `act=1.5389` `token='▁avevo'`  
   Mentre io stavo preparando la cena, lui ha telefonato per chiedermi se avevo già comprato il pane.

2. `act=1.5097` `token='▁fallait'`  
   Je lui ai dit qu’il fallait qu’on discute de l’échéance au plus vite avant la réunion.

3. `act=1.4943` `token='▁avevo'`  
   Mi ha telefonato lui per chiedermi se avevo finito il rapporto, ma non gliel'ho ancora mandato.

4. `act=1.4928` `token='▁avait'`  
   Quand sa mère lui a dit qu'elle avait besoin de faire des courses, il n'a pas insisté pour l'accompagner même s'il aurait pu proposer de l'aider.

5. `act=1.4568` `token='▁fallait'`  
   Elle leur avait dit qu’il fallait tout ranger avant que les invités n’arrivent.

6. `act=1.4564` `token='avais'`  
   Comme je n’ai pas arrêté de me plaindre de ma fatigue, le médecin m’a demandé si j’avais enfin consulté pour mon allergie au pollen.

7. `act=1.4462` `token='▁avevo'`  
   Preso l'autobus presto e, quando smontò, mi chiese se avevo fame.

8. `act=1.4194` `token='▁had'`  
   She asked the coach whether he thought the team had a chance to win the final game.

## Candidate 4: feature 13999

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.917`
- validation effect: `+0.865`
- test effect: `-0.051`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.411`

### Top natural activations

1. `act=1.1439` `token='en'`  
   L'expérimentation montre qu'en les combinant, ces forces agissent de manière inattendue.

2. `act=1.1245` `token='▁en'`  
   Está bien documentado que en la física cuántica los fenómenos observados desafían nuestra intuición clásica sobre el mundo.

3. `act=1.1087` `token='▁в'`  
   Учёные отметили, что в результате вырубки лесов под пастбища возле деревни родилась новая экосистема, где сын бывшего лесничего совместно с местными крестьянами начал использовать нетрадиционные методы управления растительностью.

4. `act=1.1030` `token='▁в'`  
   Учёные установили, что в этих условиях молекулы воды сохраняют свою структуру дольше обычного.

5. `act=1.0992` `token='▁el'`  
   Según los datos obtenidos, parece que el algoritmo está aprendiendo patrones complejos de forma autónoma.

6. `act=1.0970` `token='▁ни'`  
   После долгих размышлений и анализа данных исследователи пришли к выводу, что ни один из предложенных вариантов не подходит для реализации проекта в текущем формате.

7. `act=1.0964` `token='▁в'`  
   Много экспериментальных данных подтверждает, что в ходе лабораторных исследований новых соединений учёные всё чаще сталкиваются с тем, что результаты тестов в разных пробирках идентичны, что, в свою очередь, усиливает уверенность в правильности гипотезы.

8. `act=1.0931` `token='▁the'`  
   Given the data, we can conclude that the reaction proceeds spontaneously under standard conditions.

## Candidate 5: feature 3830

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.955`
- validation effect: `+0.988`
- test effect: `-0.331`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.361`

### Top natural activations

1. `act=1.2138` `token='▁dass'`  
   Ich dachte, du hättest gesagt, dass wir die Zugfahrt nehmen können, wenn uns der Bus nicht passt, aber jetzt sagst du, dass wir den Bus unbedingt nehmen müssen.

2. `act=1.1692` `token='▁dass'`  
   Wenn du meinst, dass diese Ausstellung wirklich etwas verändert hätte, wüsstest du sicherlich, wie man den Künstlern half, ihre Botschaft stärker zu machen.

3. `act=1.1647` `token='▁dass'`  
   Sie sagte, sie fühle sich nicht wohl, aber dass sie dennoch zum Arzt gehen werde.

4. `act=1.1628` `token='▁dass'`  
   Ich dachte, du möchtest, dass ich das Rezept übernehme.

5. `act=1.1616` `token='▁dass'`  
   Ich weiß, dass er der Künstler ist.

6. `act=1.1575` `token='▁dass'`  
   Hättest du gesagt, dass du kommen wirst, hätten wir uns freuen können.

7. `act=1.1546` `token='▁dass'`  
   Ich denke, dass es manchmal besser ist, zu warten, bis die Kinder schlafen, um das Zimmer aufzuräumen.

8. `act=1.1546` `token='▁dass'`  
   Ich denke, dass er sich nicht so gut gefühlt hat, deshalb hat er den Fußballverein verlassen und sich lieber für das Schwimmen entschieden.

---

# Variable 32: quotation_and_reported_speech_structure

- Original SAE evidence tier: **A**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 1754

- selection: `original_trainval_selected`
- train effect: `-0.830`
- validation effect: `-0.859`
- test effect: `-0.904`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.701`

### Top natural activations

1. `act=1.2483` `token='▁„'`  
   „Die Zugverbindung nach München war deutlich später als geplant“, erzählte sie, „aber das ermöglichte uns einen entspannten Aufenthalt im Bahnhofcafé.“

2. `act=1.2415` `token='▁„'`  
   Er meinte, das Rezept sei zu kompliziert, und fügte hinzu: „Einfach Salz dazu und gut ist.“

3. `act=1.2342` `token='▁„'`  
   „Es war ein unglaubliches Spiel“, erzählte mir der Trainer später, „aber ich wusste, dass sie den Sieg verdient hatten, denn ihre Leidenschaft und die Teamarbeit waren unverkennbar.“

4. `act=1.2264` `token='「'`  
   記者は会見で「すべての証拠を公開した」と述べ、疑惑を晴らす努力を強調した。

5. `act=1.2256` `token='▁„'`  
   „Mir gefällt es einfach nicht, mit dem Flugzeug zu reisen“, sagte sie und schaute zum Himmel, „die Enge, die Lautstärke – das ist für mich kein Urlaub.“

6. `act=1.2226` `token='▁„'`  
   Der Trainer betonte, dass er wisse, wie wichtig das Spiel für die Mannschaft sei, und fügte hinzu: „Wir müssen alles geben.“

7. `act=1.2111` `token='▁„'`  
   „Wir fahren morgen um acht los“, sagte sie, „und übernachten auf dem Weg in Frankfurt.“

8. `act=1.2089` `token='▁„'`  
   „Kunst spricht“, sagte sie, „aber man muss ihr zuhören lernen.“

## Candidate 2: feature 5496

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.807`
- validation effect: `-0.786`
- test effect: `-0.876`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.520`

### Top natural activations

1. `act=0.7799` `token='▁"'`  
   아버지는 놀란 얼굴로 "형이 직접 도와주시다니!"라고 반복하셨다.

2. `act=0.7478` `token='▁"'`  
   그녀는 산 정상에서 바람이 얼마나 시원한지 직접 느꼈다며 "정말 숨을 쉬기만 해도 마음이 차분해진다"고 말했고, 그 느낌은 주변의 다른 등반자들 사이에서도 공통된 감탄으로 이어졌다.

3. `act=0.7319` `token='「'`  
   彼は記者会見で「教育の公平性は私たちの使命だ」と語った。

4. `act=0.7269` `token='「'`  
   記者は会見で「すべての証拠を公開した」と述べ、疑惑を晴らす努力を強調した。

5. `act=0.7246` `token='▁"'`  
   장관은 기자들에게 "정책은 국민의 의견을 반영해야 한다"고 말했다.

6. `act=0.7231` `token='▁"'`  
   선수는 기자회견에서 "오늘 경기에서 팀원들이 최선을 다했다"고 말했다.

7. `act=0.7205` `token='▁"'`  
   어머니는 "곧 올게"라고 했다.

8. `act=0.7194` `token='「'`  
   記者会見で彼は「今後の対応については内閣で最終的に判断する」と述べた。

## Candidate 3: feature 2323

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.831`
- validation effect: `-0.875`
- test effect: `-0.910`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.453`

### Top natural activations

1. `act=1.7875` `token='sie'`  
   Doch auch wenn wir in der KI-Forschung oft „sie“ meinen, wenn wir über neuronale Netzwerke sprechen, ist es wichtig zu erkennen, dass nicht immer „dieses sie“ dieselbe Rolle oder Funktion hat wie jenes „sie“, das im Alltagskontext gemeint ist.

2. `act=1.7721` `token='俺'`  
   「彼が昨日会社を辞めたって言ってたけど、ほんと？いつからだっけ？どうして？」「詳しく話してないみたいで、ただ『俺にはこれ以上続ける理由がない』って言って去っていったんだってさ。」

3. `act=1.7597` `token='ben'`  
   Ah be ne çaresizlik! Bugün sabah işe girdim ki kafama vurdu da bu ofiste kimse "ben gelmiş olsaydım" diye düşünsen fena olmazdı ama herkes başka bir dünya da gibi konuşuyor sanki, ben herşeyi düzeltmem gerekeni sanıyor da, aslında işler zaten hepinizin elinde bozuk!

4. `act=1.7279` `token='今日'`  
   「試合のあとで選手が『今日の守備はチーム全員でやるべきだった』と話していた」と応援団のリーダーが言ってました。

5. `act=1.6928` `token='Sie'`  
   Sie begrüßte den Professor stets mit „Sie“ und höchstem Respekt.

6. `act=1.6905` `token='Sie'`  
   Frau Meier bat mich höflich, sie mit „Sie“ anzusprechen.

7. `act=1.6825` `token='ka'`  
   Tahliye kararını kimin verdiğini sorduğumda savcı, "Ben değilim, başka bir makam" diye cevap verdi ama bu kez ben de cevabının yetersiz olduğunu belirterek "O 'başka' kimdir?" dedim.

8. `act=1.6792` `token='вы'`  
   Мне приятно, когда меня зовут на уважительное "вы", особенно на спортивных тренировках.

## Candidate 4: feature 15531

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.817`
- validation effect: `-0.844`
- test effect: `-0.893`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.337`

### Top natural activations

1. `act=1.1571` `token='。」'`  
   「この辺りの蕎麦屋は、地元のおじいちゃんがよく『味噌汁無料でつけてくれるんだ』って言ってるよ。」

2. `act=1.1507` `token='。」'`  
   「この駅は本当に混んでいて、前の電車に間に合わなかった友達が『次のものには絶対乗らないとまずいよ』って言っていました。」

3. `act=1.1449` `token='。」'`  
   「この絵画は、都会の喧騒の中で見つける静けさを表現しています。」と、館長は説明してくれた。

4. `act=1.1352` `token='。」'`  
   「最近、この地域の山で奇妙な音が聞こえるという話を耳にしたんだけど、実際に聞いてみたかったら、天気の良い日に朝早くから森の中に入ってみるのがいいって言ってたよ。」

5. `act=1.1305` `token='。」'`  
   「この駅の食堂で、隣の人が『東京のラーメンはここよりダシが濃いって言うけど、本当かな？』と話していました。」

6. `act=1.1297` `token='。」'`  
   「今夜、美術館で展示が始まるから、ぜひ見てみて。」と彼女は話した。

7. `act=1.1275` `token='。」'`  
   「この観光バスは、観光客の多くが楽しんでいる富士山の絶景を堪能できるように、ツアーの最後のほうに休憩時間を組み込んでいるんです。」

8. `act=1.1180` `token='。」'`  
   「昨日の練習では、コーチが『体の軸をしっかり立てないと、ボールはうまく打てないよ』と繰り返し言ってたけど、その通りだなあ。」

## Candidate 5: feature 11822

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.819`
- validation effect: `-0.865`
- test effect: `-0.897`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.744`

### Top natural activations

1. `act=1.4594` `token='▁`'`  
   After adjusting the parameters in the recipe file named `desserts_v4_2025.csv`, the system flagged several inconsistencies in the portion sizes listed under the `savory_sides` category using the hashtag #PortionMismatch.

2. `act=1.3564` `token='▁„'`  
   Mir ist aufgefallen, wie sie mit dem Chef immer „Sie“ sagt, aber mit Kollegen um die gleiche Altersstufe eher locker und informell redet.

3. `act=1.3530` `token='▁„'`  
   Der Katalog des Museums ist unter „M_Kat2024“ im Archiv abgelegt.

4. `act=1.3480` `token="▁'"`  
   En la fórmula que propuse ayer, el uso del parámetro 'x' en conjunto con el operador de derivada lo expresa claramente.

5. `act=1.3336` `token='▁„'`  
   Herr Professor Doktor Müller verbot es mir strikt, ihn mit „Sie“ anzureden, doch bei der nächsten Vorlesung fragte er mich überraschenderweise auf Du.

6. `act=1.3320` `token='▁„'`  
   Das Dokument mit dem Namen „Bericht_Q3_2023.pdf“ wurde in den Ordner „Finanzen“ hochgeladen, um es für die nächste Meeting-Vorbereitung leicht zugänglich zu halten.

7. `act=1.3306` `token='▁„'`  
   Ich habe gerade eine alte Hausaufgabe aus dem Ordner „Mathe_SS2023“ gefunden und sie online mit dem Hashtag #SchulzeitErinnerung geteilt.

8. `act=1.3286` `token='▁„'`  
   Der Forschungsprojektbericht wurde unter dem Namen „SozialInteraktion_2023_KohorteB“ im Ordner „/Dokumente/Psychologie_Studien/“ gespeichert, um ihn später mit den anderen Dateien wie „HashtagAnalyse_#SozialeMedien“ oder „Ergebnisse_TeilA_01“ zu vergleichen.

---

# Variable 33: discourse_relation_marking

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.200**

## Candidate 1: feature 9728

- selection: `original_trainval_selected`
- train effect: `-0.881`
- validation effect: `-0.112`
- test effect: `+0.886`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.946`

### Top natural activations

1. `act=0.9670` `token='▁oyuncu'`  
   Fenerbahçe oyuncuları, zorlu müsabakada hem savunma hem de hücum açısından dengeli bir oyun ortaya koyarak rakibini yenmeyi başardılar.

2. `act=0.6997` `token='▁नदी'`  
   बच्चे नदी के किनारे एक पत्थर को हिलाते हुए उसमें से छिपे हुए मछलियों को देखने लगे।

3. `act=0.6829` `token='▁Koch'`  
   Koch uns etwas zu essen.

4. `act=0.6815` `token='▁Taking'`  
   Taking care of your health means getting enough rest and eating well every day.

5. `act=0.6815` `token='▁Taking'`  
   Taking vitamin C regularly can prevent colds but will not cure them.

6. `act=0.6815` `token='▁Taking'`  
   Taking daily vitamins can improve overall wellness.

7. `act=0.6795` `token='▁konuy'`  
   Öğrenciler konuyu önce ayrıntılı olarak öğrendikten sonra uygulama ödevlerine geçtiler.

8. `act=0.6736` `token='▁Now'`  
   Now the rain has moved east of the river.

## Candidate 2: feature 9675

- selection: `train_fwer_only`
- train effect: `-0.881`
- validation effect: `+0.069`
- test effect: `+0.919`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.941`

### Top natural activations

1. `act=1.1256` `token='▁我們'`  
   我們明天早上七點出發。

2. `act=1.1256` `token='▁我們'`  
   我們打算坐高鐵去台北，出發前你得先打電話確認一下班次時間，這樣到了月台才不會發現錯過了最後一班車。

3. `act=1.1256` `token='▁我們'`  
   我們馬上啟程去機場。

4. `act=1.1047` `token='▁Mah'`  
   Mahkeme, yetki alanının genişletilmesi talebini reddetmekle kalmadı, aynı zamanda ilgili kişiyle özel bir görüşme yapmak için zorunlu kılma kararı aldı.

5. `act=1.0864` `token='▁प्रबंध'`  
   प्रबंधक ने कर्मचारियों से अपनी मौजूदा जिम्मेदारियाँ साझा करने को कहा।

6. `act=1.0864` `token='▁प्रबंध'`  
   प्रबंधन ने प्रस्ताव को मंजूरी दे दी।

7. `act=1.0821` `token='▁숙'`  
   숙제로 제주도 여행 계획을 갑자기 바꾸다니 참 신기하네.

8. `act=1.0821` `token='▁숙'`  
   숙부가 여행 중에 할아버지와 함께 유럽의 오래된 도시를 방문했고, 그들은 서로 다른 방식으로 도시의 문화와 역사에 깊이 매료되었다.

## Candidate 3: feature 4016

- selection: `train_fwer_only`
- train effect: `-0.882`
- validation effect: `+0.170`
- test effect: `+0.906`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.935`

### Top natural activations

1. `act=1.3228` `token='▁تعمل'`  
   تعمل زميلتي الاثنتان في مكتب صغير إلى جانبي، وتتحدثان بهدوء حول توزيع المهام بينهما لمشروع عمل يشتركان فيه.

2. `act=1.3228` `token='▁تعمل'`  
   تعمل مدرسة اللغة على تطوير كفاءات الطلاب بشكل فعّال.

3. `act=1.3228` `token='▁تعمل'`  
   تعمل المدرسة التقنية على تطوير نموذج جديد للمفاعل النووي مع تصميم دقيق للمعدات والمعايير.

4. `act=1.3228` `token='▁تعمل'`  
   تعمل المكابس الثنائية بفعالية في تدوير النفايات.

5. `act=1.3228` `token='▁تعمل'`  
   تعمل الكثافات العالية للمياه المالحة على تشكيل طبقات مستقرة في قاع البحر.

6. `act=1.3228` `token='▁تعمل'`  
   تعمل المدرسة على حماية الغابات الناضجة من التآكل البيئي من خلال تنفيذ مشاريع استدامة وتعليمية.

7. `act=1.3228` `token='▁تعمل'`  
   تعمل المدرسة على تطوير مهارات الطلاب بجوار التميز الأكاديمي.

8. `act=1.3228` `token='▁تعمل'`  
   تعمل المفتاحان اللذان يكوِّنان زوجًا متزامنًا على تأمين الاتصال الرقمي.

## Candidate 4: feature 7036

- selection: `train_fwer_only`
- train effect: `-0.883`
- validation effect: `+0.073`
- test effect: `+0.927`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.922`

### Top natural activations

1. `act=1.6539` `token='▁#'`  
   #İşRaporu_ÇalışanA_B203 dosyasını kontrol etmeden genel müdürle toplantı yapmamak elde değil.

2. `act=1.6539` `token='▁#'`  
   #HayvanatBahçesiProjesi yarışması için başvuru dosyası tamamlandı.

3. `act=1.6539` `token='▁#'`  
   #CumhurbaşkanlığıSosyalMedyaHesabıNDanSonDuyuru

4. `act=1.6539` `token='▁#'`  
   #SağlıklıYaşam2023 projemiz kapsamında düzenlediğimiz etkinliğe 50'den fazla birey katıldı.

5. `act=1.6539` `token='▁#'`  
   #ElmaSorusu çözümünü masaya koydum.

6. `act=1.6394` `token='▁Manche'`  
   Manche Patienten nehmen jedes Medikament sorgfältig ein, andere verschlucken alle Tabletten auf einmal.

7. `act=1.6375` `token='▁Long'`  
   Long-term exposure to air pollution can significantly affect children's respiratory development and increase the likelihood of chronic health conditions later in life.

8. `act=1.6375` `token='▁Long'`  
   Long-distance trains typically operate efficiently across multiple countries, offering passengers a comfortable and environmentally friendly alternative to air travel for extended journeys between major cities.

## Candidate 5: feature 2668

- selection: `train_fwer_only`
- train effect: `-0.879`
- validation effect: `+0.165`
- test effect: `+0.937`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.921`

### Top natural activations

1. `act=1.5802` `token='▁문제를'`  
   문제를 일으킨 기관은 책임을 회피하려고 했다.

2. `act=1.5532` `token='▁Руководство'`  
   Руководство компании отрицает, что будут сокращать штат в этом квартале.

3. `act=1.5532` `token='▁Руководство'`  
   Руководство компании решило нанять новых сотрудников, включая и иностранцев, для расширения отдела разработки.

4. `act=1.5530` `token='▁다'`  
   다니시겠습니까, 김부장님?

5. `act=1.5530` `token='▁다'`  
   다 먹다 싶었는데 밥이 뜨거워서 놀랐어.

6. `act=1.5352` `token='▁방문'`  
   방문한 옛 집에서 삼촌은 사진 액자들을 하나씩 들며 추억을 떠올렸다.

7. `act=1.5225` `token='▁Käsi'`  
   Käsi-kirjaimilla kirjoitettu tarina oli kauniimmainen kuin levyn kansi.

8. `act=1.5225` `token='▁Käsi'`  
   Käsittääkseni perunat kuivattuina tai rapussa ovat välttämättömästi mukana ruoanlaiton suunnitelmaa hahmottellessa, mutta joskus sellaisen aineksen tarve on mahdollinen myös muissa kotitalousyhteyksissä, kuten kevyen herkutuksen valmistuksessa.

---

# Variable 34: topic_comment_structure

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **1.000**

## Candidate 1: feature 10896

- selection: `original_trainval_selected`
- train effect: `-0.680`
- validation effect: `-0.290`
- test effect: `-0.609`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.470`

### Top natural activations

1. `act=1.3581` `token='▁#'`  
   项目文档需要按照最新版本的格式上传到共享文件夹，例如 "2023年度-Q4_KPI评估报告_v2.1.pdf"，并且在邮件主题中加上 #内部会议_11月9日 以便统一归档。

2. `act=1.3389` `token='▁#'`  
   Der Patient hat die Befunde unter dem Hashtag #FallID_45B12 auf der internen Plattform abgelegt.

3. `act=1.3350` `token='▁#'`  
   Am Montagabend stieß die Familie Meier-Steinberg auf den Hashtag #Familienfest2023, der die Einladung zur zentralen Feierlichkeit im Rathausplatz erklärte.

4. `act=1.3342` `token='▁#'`  
   Ich habe gerade die Datei „Rezepte_Oktober2023.pdf“ auf meinem Laptop gespeichert und sie gleich mit dem Hashtag #Sommergerichte getaggt.

5. `act=1.3198` `token='▁#'`  
   Die neuen Lehrpläne für das Gymnasium sind unter dem Hashtag #GymLehrplan2024 auf der offiziellen Schulhomepage einsehbar.

6. `act=1.3145` `token='▁#'`  
   After adjusting the parameters in the recipe file named `desserts_v4_2025.csv`, the system flagged several inconsistencies in the portion sizes listed under the `savory_sides` category using the hashtag #PortionMismatch.

7. `act=1.3098` `token='▁#'`  
   Ich habe gerade eine alte Hausaufgabe aus dem Ordner „Mathe_SS2023“ gefunden und sie online mit dem Hashtag #SchulzeitErinnerung geteilt.

8. `act=1.3082` `token='▁#'`  
   L'employé a envoyé un rapport détaillé intitulé "AnalyseQ4_2023_RH@departement.xlsx" à la direction via l'intranet, en incluant un commentaire avec le hashtag #ProjetsClés pour faciliter le suivi par l'équipe de gestion.

## Candidate 2: feature 6760

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.686`
- validation effect: `-0.405`
- test effect: `-0.726`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.253`

### Top natural activations

1. `act=1.4411` `token='▁in'`  
   Der Professor erklärte den Studenten, dass die Forschungsergebnisse laut einer KI-Analyse „einen klaren Zusammenhang zwischen neuronalen Mustern und kreativem Denken zeigen“, was in der Fachwelt heftig diskutiert werde.

2. `act=1.3593` `token='▁in'`  
   Künstlerischen Ausdruck zu fördern, ist in vielen Kulturen ein Weg, gesellschaftliche Werte zu vermitteln.

3. `act=1.3308` `token='▁in'`  
   Die Zugverbindung von Berlin nach München, die in der Regel zwei Stunden und dreißig Minuten beträgt, wird aufgrund eines technischen Defekts um über eine Stunde verlängert, sodass Reisende alternative Verkehrsmittel in Betracht ziehen sollten.

4. `act=1.2977` `token='▁in'`  
   Um die genetischen Grundlagen komplexer Verhaltensweisen innerhalb einer Tierart zu verstehen, analysieren Forscher oft langfristig festgelegte Paarungsbeziehungen, die in solchen Populationen typischerweise lebenslang bestehen.

5. `act=1.2972` `token='▁in'`  
   Es wird in der Pressekonferenz betont, dass im Zuge der Reformen nicht ausgeschlossen sei, dass die Zuständigkeiten neu verteilt werden müssten, um Effizienz und Transparenz in den öffentlichen Dienst zu steigern.

6. `act=1.2912` `token='▁in'`  
   Die Pollenflugperiode, die jedes Jahr im Frühling aufgrund des sich erwärmenden Klimas um etwa zwei Wochen voranschreitet, wird in der aktuellen Studie aktiv von den Wissenschaftlern überwacht und analysiert, um mögliche Auswirkungen auf die Allergiebelastung der Bevölkerung zu bewerten.

7. `act=1.2845` `token='▁in'`  
   Selbstverständlich, die Quantenteilchen, von denen du sprichst, weisen aufgrund ihrer Superpositionseigenschaften interessante Verhaltensweisen auf, die in klassischen Physikmodellen nicht vorkommen.

8. `act=1.2781` `token='▁in'`  
   Die verschiedenen Techniken und Materialien, aus denen die Wandteile des barocken Theaters in Dresden restauriert wurden, sind in einer detaillierten Dokumentation zusammengefasst worden.

## Candidate 3: feature 2509

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.868`
- validation effect: `-0.578`
- test effect: `-0.709`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.227`

### Top natural activations

1. `act=1.1492` `token='いつも'`  
   私より上の立場のお客様には、いつも敬語で接するよう心がけています。

2. `act=1.1319` `token='いつも'`  
   お世話になっております、田中料理長にはいつもおいしいお弁当を届けていただいております。

3. `act=1.1261` `token='いつも'`  
   先生には、いつも丁寧にお願いいたします。

4. `act=1.1168` `token='いつも'`  
   事務所の窓辺にはいつも小さな観葉植物がいくつか置いてあり、それを見ると一息つくことができる。

5. `act=1.1168` `token='すぐに'`  
   その件については、すぐに連絡してください。

6. `act=1.1068` `token='いつも'`  
   山田コーチには、いつも敬意をもって接しています。

7. `act=1.0991` `token='めて'`  
   この度、ご案内いただいた観光バスツアーは大変貴重な経験となりましたが、社長先生には改めて御礼申し上げます。

8. `act=1.0979` `token='いつも'`  
   課長にはいつも丁寧に挨拶するように心がけています。

## Candidate 4: feature 1302

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.779`
- validation effect: `+0.534`
- test effect: `+0.694`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.094`

### Top natural activations

1. `act=1.7424` `token='üyor'`  
   Akasya ağacının yaprakları bu kadar kuru olsa bile hâlâ yeşil görünüyor.

2. `act=1.7343` `token='lanıyor'`  
   Ders anlatımı devam ederken öğrencilerin çoğu dikkatini toplamakta zorlanıyor ve sunulan bilgileri sürekli olarak hatırlamaya çalışıyor.

3. `act=1.7300` `token='üyor'`  
   Karınca ısırığından zarar gören komşumun derisi hâlâ kızarık görünüyor.

4. `act=1.7272` `token='üyor'`  
   Hiçbir bilim adamı o olayı gözlemlemedi ve bu da yazarın teorisinin yanlış olduğuna dair güçlü bir kanıt gibi görünüyor.

5. `act=1.7126` `token='lanıyor'`  
   Bir sonraki etkinlikte öncelikle daha önce görülmemiş bir sanat projesi olarak kabul edilen bir eserin, nasıl yaratıldığı ve etkisi nasıl geliştiği konusunda öğrencilere anlatılması planlanıyordu.

6. `act=1.7051` `token='üyor'`  
   Yakın zamanda yapılan bir araştırmada, öğrencilerin performansı sınıf ortamının bireyselleştirilmesiyle artmış olmalı çünkü bu durum bireysel ihtiyaçlara daha fazla dikkat edilmesine yol açar gibi görünüyor.

7. `act=1.7047` `token='üyor'`  
   Proje dosyası olan "YeniYetenek_v1.py" içinde hata var gibi görünüyor.

8. `act=1.6979` `token='▁ediliyor'`  
   Kamuoyunun en çok konuştuğu haberde, kaynaklar arasında yer alan bakan yardımcısı tarafından doğrulandığı rivayet edilen açıklamada, mahkemeye sunulan yeni belgelerin siyasi ittifakın iç ayaklanmasını göstereceği iddia ediliyor.

## Candidate 5: feature 11611

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.795`
- validation effect: `-0.574`
- test effect: `-0.855`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.091`

### Top natural activations

1. `act=1.2986` `token=','`  
   시청에서 생활폐기물 분리수거 안내문을 다시 작성해달라는 요청이 들어왔는데, 이번에는 주부들 사이에서 오해가 있었던 내용이라 조금 더 자세히 설명하고 예외 조건도 명확히 해야겠다는 생각이 든다.

2. `act=1.2560` `token='、'`  
   母に電話で、今週末に私たち家族が東京ドームの近くのホテルに泊まることになったので、お父さんと妹を連れてその辺りを一緒に散歩してみないかと誘ってみたいと思っているんだけど、どう思う？

3. `act=1.2173` `token='、'`  
   「昨日、母が『このレシピは絶対に失敗しない』って言って、新しく買った電動ミキサーを使ってケーキを焼いたんだけど、なんだかうまくいかなかったんだよね。」

4. `act=1.2057` `token=','`  
   మా బృందం కలసి ఒక పెద్ద నాటకం చేయడం గురించి చిత్రణను తయారుచేస్తున్నాం కాబట్టి, ఆహ్వానించాలని భావిస్తున్నాం.

5. `act=1.2027` `token=','`  
   형이 갑자기 연락을 해서 집에 가라고 했는데, 왜 그런지 전혀 예상 못해서 놀랐어요.

6. `act=1.1970` `token=','`  
   여름 휴가를 보내기 위해 시골에 있는 할아버지 집으로 가려고 하는데, 길이 너무나 좁아서 큰 차는 들어갈 수 없어 현지인들에게 도움을 요청해 작고 컴팩트한 차를 빌렸다.

7. `act=1.1931` `token='、'`  
   昨日、新しい自転車が届いたんだけど、すでに友達が二台借りていったんだ。

8. `act=1.1882` `token=','`  
   어머니께 그림 전시에 초대장을 드리고 싶은데, 어떻게 여쭤보아야 할지 망설입니다.

---

# Variable 35: focus_and_given_new_marking

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.928**

## Candidate 1: feature 7136

- selection: `original_trainval_selected`
- train effect: `+0.699`
- validation effect: `+0.419`
- test effect: `+0.102`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.345`

### Top natural activations

1. `act=1.3807` `token='が'`  
   ここで資料を確認しているんだけど、あそこはまだ整理が終わっていないから、後で戻ってくるようにしておく。

2. `act=1.3354` `token='が'`  
   今日は朝から気持ちが重くて、コーヒーを淹れても少しは明るくならなかったけど、散歩に出かけたら空が青くて鳥の鳴き声が聞こえて、何となく心が軽くなった。

3. `act=1.3152` `token='が'`  
   昨日試合を見に行ったんですけど、チームの選手たちが全体的に動きが重たくて、攻撃の流れを作るのがすごく難しかったなあと思いました。

4. `act=1.2861` `token='이'`  
   여행 중에 물을 너무 부드럽게 데친 탓에 속이 울리는 것 같아요.

5. `act=1.2854` `token='が'`  
   ここ数日、職場の安全体制について改めて見直しが進められている。

6. `act=1.2843` `token='이'`  
   아니, 저 산 정상에 눈이 이렇게 많이 쌓였단 말인가!

7. `act=1.2750` `token='이'`  
   버스를 타고 길을 가는데, 아침에 눈이 왔다는 소식이 나와서 정말 놀랐어.

8. `act=1.2554` `token='が'`  
   「今日はあまり具合が良くないんだ。」

## Candidate 2: feature 15357

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.704`
- validation effect: `-0.185`
- test effect: `-0.407`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.313`

### Top natural activations

1. `act=0.5808` `token='▁बह'`  
   आपकी छोटी बहन कुछ पानी के साथ ताज़ा हरी पत्तियाँ लाएँगी।

2. `act=0.5753` `token='踏'`  
   彼女は地元のガイドに道を尋ねるために小さなカフェで時間を過ごし、その思いやり深い提案によって、通りの向こうにある隠れた公園に足を踏み入れることになった。

3. `act=0.5686` `token='踏'`  
   昨日の野球の試合では、よく走る選手がホームベースを踏みながらも盗塁を成功させたのが、観客に大きな驚きと拍手をもたらしました。

4. `act=0.5655` `token='踏'`  
   芸術祭が成功裏に終わり、市長はその評価を踏まえて、来年の予算案の中でさらに文化振興のための資金を増やすよう提案した。

5. `act=0.5652` `token='踏'`  
   小説を読むのが好きな友人は、日本映画や演劇の魅力についてもよく語るが、私自身はその世界にあまり踏み込んだ経験がなく、彼女の話を聞いていても具体的なイメージがなかなか湧かないことがある。

6. `act=0.5622` `token='▁тро'`  
   У туристов, путешествующих по горной тропе в Крыму, часто возникает необходимость приобрести местные сувениры или продовольствие, так как вещи легко теряются или расходуются в пути.

7. `act=0.5464` `token='▁бол'`  
   Все врачи вместе придумали комплексное лечение для пациентов с редкими болезнями.

8. `act=0.5411` `token='踏'`  
   ご予算とスケジュールの都合を踏まえつつ、公共交通機関を利用した移動プランの最適化を依頼いたします。

## Candidate 3: feature 209

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.700`
- validation effect: `+0.162`
- test effect: `+0.038`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.297`

### Top natural activations

1. `act=1.3128` `token='が'`  
   漢字と仮名が交じる文章を読むとき、文節の切れ目が自然に理解できるようになるには、語彙の知識が不可欠である。

2. `act=1.2999` `token='が'`  
   ここで資料を確認しているんだけど、あそこはまだ整理が終わっていないから、後で戻ってくるようにしておく。

3. `act=1.2946` `token='が'`  
   会議でプレゼンテーションをする前に、資料の確認が終わっていなかったため、チームメンバーに急遽意見を聞いた。

4. `act=1.2930` `token='が'`  
   先生のご指導のおかげで、日本の学校の授業についてもっと自信が持てるようになりました。

5. `act=1.2930` `token='が'`  
   彼女は論文を書いている途中で、資料の整理がずさんだったことに気づいた。

6. `act=1.2566` `token='が'`  
   「新しい教育改革の提案について、政策立案者たちは議論を深めながらも、実現可能性を巡る疑問点や地域ごとの実情への配慮が十分に議論されず、国民全体への周知と説明責任が見過ごされているのではないかという声が高まっている。」

7. `act=1.2555` `token='が'`  
   彼は担当者に指示を出して、最終的に役所の手続きが進まなかった。

8. `act=1.2518` `token='が'`  
   彼は漢字の成り立ちを教わってから、日本語の学びがより楽しくなった。

## Candidate 4: feature 8334

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.702`
- validation effect: `+0.381`
- test effect: `-0.034`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.138`

### Top natural activations

1. `act=1.1335` `token='이'`  
   그 경기, 우리 팀이 이겼다.

2. `act=1.1137` `token='이'`  
   어제 경기에서 우리 팀이 이겼어요.

3. `act=1.1137` `token='이'`  
   정말 황당하게도 이 경기에서 우리 팀이 역전승을 했어.

4. `act=1.0957` `token='이'`  
   선수는 "우리 팀이 다음 경기에서 반드시 이길 수 있다"고 말했다.

5. `act=1.0881` `token='이'`  
   어머, 우리 팀이 이겼다니 정말 놀랍네요!

6. `act=1.0881` `token='이'`  
   어머, 우리 팀이 오늘 경기에서 이겼대요?

7. `act=1.0878` `token='이'`  
   그 경기에서 우리 팀이 이겼지만, 후반에 패배 위기를 맞기도 했다.

8. `act=1.0789` `token='이'`  
   우리팀이 연장전까지 갔음에도 불구하고 결국 경기를 이겼다는 소식을 들었을 때 감독님의 표정은 깊은 놀라움과 동시에 성취감으로 가득 차 있었다.

## Candidate 5: feature 3848

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.699`
- validation effect: `+0.681`
- test effect: `+0.564`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.982`

### Top natural activations

1. `act=1.2442` `token='が'`  
   どの駅が最寄りですか。

2. `act=1.2442` `token='が'`  
   どの駅が便利ですか。

3. `act=1.2380` `token='を'`  
   「この薬を飲むと、すぐに効果が出るとは限りませんよ」と医者は優しく言いながら、彼女はそれでも少し不安そうだった。

4. `act=1.2021` `token='を'`  
   この薬を服用する前には、必ず医師に相談してください。

5. `act=1.2021` `token='を'`  
   この薬を飲むのを忘れてしまったんですけど、今からでも間に合うと思います。

6. `act=1.2021` `token='を'`  
   この薬を飲んだあとで、熱もだいぶ下がって体も楽になった。

7. `act=1.2021` `token='を'`  
   この薬を渡すと、彼はすぐに元気になるはず。

8. `act=1.2021` `token='を'`  
   この薬を服用してから、彼女の体調が大きく改善した。

---

# Variable 36: genericity_and_kind_level_reference

- Original SAE evidence tier: **B2**
- Probe core status: **robust_3of3**
- Layer-12 mean delta probe test AUROC: **0.937**

## Candidate 1: feature 5836

- selection: `original_trainval_selected`
- train effect: `+0.372`
- validation effect: `+0.233`
- test effect: `+0.345`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `2`
- specificity ratio: `0.613`

### Top natural activations

1. `act=0.9128` `token='mattomi'`  
   Tämä kisaveikotus, jossa perinteiset liikehuollon menetelmät yhdistyvät uusiin teknologisiin ratkaisuihin, on omalta osaltani osoittautunut erinomaiseksi keino vähentää loukkaantumisriskiä lajin parissa kouluttamattomilta käyttäjiltäkin.

2. `act=0.7899` `token='щему'`  
   Сотрудник передал документ неработающему принтеру.

3. `act=0.7884` `token='neen'`  
   Kun pysähtyi lähimmän buspysäkön ääreen, huomasi että matkustajat olivat kaikki vielä tyytyväisiä ja että huoltaja oli juuri saapunut vaihtamaan pölyhermosta kärsineen linjan vetämään liikenteeseen.

4. `act=0.7702` `token='▁हुए'`  
   हमारे परिवार में दिन के भोजन के लिए आमतौर पर चावल, दाल, सब्जी और एक अचार या प्याज की चटनी की जरूरत होती है, जबकि रात का खाना थोड़ा भिन्न होता है, जैसे आज हमने रात के खाने में पूरे गेहूं के लड्डू और एक तले हुए मसालेदार बैगरे का विकल्प चुना।

5. `act=0.7572` `token='вшим'`  
   На стоянке у пожарной части припаркована ещё одна машина с горевшими фарами и повреждённым бампером.

6. `act=0.7562` `token='aked'`  
   A sudden downpour had drenched the forest floor, leaving it glistening and fragrant with the unmistakable freshness of rain-soaked earth.

7. `act=0.7465` `token='ed'`  
   I never realized how much I missed the taste of home-cooked soup until it was gone.

8. `act=0.7395` `token='en'`  
   Walking along the riverbank, we spotted a kingfisher perched on a weather-beaten wooden pier.

## Candidate 2: feature 1858

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.366`
- validation effect: `+0.344`
- test effect: `+0.475`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.901`

### Top natural activations

1. `act=1.0040` `token='ов'`  
   Ни один из ресторанов поблизости не предлагает действительно вкусную и недорогую еду, ни в завтраке, ни в обеде, и туристы разочарованно покидают площадь.

2. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n’a mangé tous les gâteaux.

3. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n’a terminé toutes les tâches qu’on leur avait assignées.

4. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n’ont été autorisés à participer sans que leurs parents ne soient présents.

5. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n'avait eu l'intention de s'absenter de la réunion familiale, mais tout le monde savait que chaque personne y participerait à sa manière.

6. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n’a touché la fleur rare que j’avais plantée au fond du jardin.

7. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants ne semble ignorer les consignes de sécurité.

8. `act=0.9858` `token='▁enfants'`  
   Aucun des enfants n’a voulu manger les légumes.

## Candidate 3: feature 13521

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.388`
- validation effect: `+0.303`
- test effect: `+0.465`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.650`

### Top natural activations

1. `act=0.7584` `token='▁ने'`  
   कार्यालय में दो नए कर्मचारी आए हैं और तीन पुराने सभी ने सीखा।

2. `act=0.7521` `token='▁had'`  
   Exactly three of the participants had prior experience with quantum computing protocols.

3. `act=0.7167` `token='▁seem'`  
   None of the characters in the play actually seem to want to change their lives.

4. `act=0.6975` `token='▁had'`  
   The meeting was scheduled for 3:00 PM, but by 3:45, only two team members had arrived.

5. `act=0.6836` `token='en'`  
   Alle drei Patienten erhielten je ein zusätzliches Medikament, doch nur zwei zeigten Besserung.

6. `act=0.6790` `token='▁showed'`  
   In the genetic analysis, three pairs of twins showed similar inheritance patterns across five generations of their extended family lineage.

7. `act=0.6783` `token='▁haben'`  
   Drei von den fünf Teilnehmerinnen haben sich einzeln gegen alle anderen durchgesetzt, während zwei andere gemeinsam eine Koalition gebildet und damit versucht haben, die Ergebnisse der Diskussionen zu beeinflussen.

8. `act=0.6707` `token='▁had'`  
   None of the players on the team had failed to notice the new coach's intense focus during practice.

## Candidate 4: feature 142

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.338`
- validation effect: `+0.336`
- test effect: `+0.471`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `4`
- specificity ratio: `0.693`

### Top natural activations

1. `act=2.0374` `token='▁%'`  
   Según el informe del ministerio, el 70 % de los hogares redujo el consumo de azúcar en los últimos meses.

2. `act=1.8915` `token='▁%'`  
   Un estudio reciente reveló que el 70 % de los adultos con hipertensión no siguen una dieta saludable.

3. `act=1.8824` `token='▁%'`  
   Se estima que más del 80 % de los viajeros que utilizan el tren nocturno entre Madrid y Barcelona optan por dormir en cabinas privadas compartidas con un compañero de viaje elegido al azar para garantizar una experiencia social única durante el trayecto.

4. `act=1.8702` `token='▁60%'`  
   في دراسة حديثة أجرتها جامعة القاهرة، تبين أن حوالي 60% من الشباب العربي مهتمون بمتابعة التطورات في مجال التكنولوجيا والتعليم.

5. `act=1.8489` `token='▁ciento'`  
   Un estudio reciente reveló que el 60 por ciento de los votantes apoyan la propuesta del gobierno para aumentar las licencias parentales.

6. `act=1.8281` `token='▁60%'`  
   Според изследването на института за образование, над 60% от студентите заявяват, че виртуалното обучение е по-ефективно от традиционното.

7. `act=1.8277` `token='▁30%'`  
   Според изследването на университета, около 30% от студентите са заявили, че предпочитат онлайн обучението.

8. `act=1.8176` `token='ers'`  
   A recent survey suggests that roughly three-quarters of households regularly consume plant-based milk alternatives, indicating a notable shift in dietary preferences toward health-conscious choices and environmental sustainability.

## Candidate 5: feature 2022

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.348`
- validation effect: `+0.354`
- test effect: `+0.419`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `5`
- specificity ratio: `0.630`

### Top natural activations

1. `act=1.6854` `token='▁çok'`  
   Yarın akşam etkinliğe katılmamayı düşündüğümde, çok fazla heyecanlanıyorum ama aynı zamanda biraz da endişeliyim çünkü önceden bir araya geldiğimiz insanların hepsi çok samimi ve sıcak bir ruhlarla doluymuş.

2. `act=1.6841` `token='▁çok'`  
   Kızı için doğum gününde yeni bir ayakkabı aldı ama çok pahalı geldiğinden dolayı ikinci el mağazasından sadece birkaç günlüğüne ödün verdi.

3. `act=1.6804` `token='▁çok'`  
   Sık sık sokak kediğine yemek verdiğim parkta, bahçelerini tarif etmeyi sevdiğim yaşlı bayana çay içirirken, soluk almak için zaman zaman gelen giden çocuklar ve koşu yapan yaşlı çiftlerle birlikte geçirdiğim son yaz günleri, aslında çok daha önce başlayan bu alışkanlıklarımın hâlâ devam ettiğini fark etmeden hissettim.

4. `act=1.6604` `token='▁много'`  
   След като чухме мъжкия си говор вчера, сигурно ще се подготвим добре за изпита по история утре, защото той е много опитен и често казва истината.

5. `act=1.6519` `token='▁çok'`  
   Köpeğim sonunda iyileşti ama çok zorlandığını bir daha düşünmemek istiyorum.

6. `act=1.6508` `token='▁çok'`  
   Bugün sokakta tanıştığımız yaşlı bayan, bize çay içirmek istediğini ve birlikte konuk odasına geçmemizi söylediğinde çok şaşırdık.

7. `act=1.6474` `token='▁çok'`  
   Arkadaşımı görmek için akşam yemeğine gittim ama çok şanslı değildim.

8. `act=1.6418` `token='▁çok'`  
   İspanya'daki tarihi yerleri gezmek için geçen yaz buraya geldiğimde, çok farklı bir atmosfer olduğunu fark ettim.

---

# Variable 37: social_deixis_honorifics_status_encoding

- Original SAE evidence tier: **B2**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.750**

## Candidate 1: feature 2081

- selection: `original_trainval_selected`
- train effect: `+0.820`
- validation effect: `+0.422`
- test effect: `+0.372`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.771`

### Top natural activations

1. `act=1.0666` `token='습니다'`  
   정부는 아동들의 건강한 식습관을 형성하기 위해 학교 급식 메뉴에서 인스턴트 식품의 제공을 제한하도록 지자체에 지침을 내렸습니다.

2. `act=1.0235` `token='했습니다'`  
   정부 정책에 대해 여론은 갈리기 시작했습니다.

3. `act=1.0224` `token='했습니다'`  
   그는 학생들이 발표에 대해 더 많이 토론하도록 환경을 조성했습니다.

4. `act=1.0035` `token='했습니다'`  
   실험실에서 그들은 화학 반응을 촉진하도록 특별한 촉매를 사용했습니다.

5. `act=0.9712` `token='습니다'`  
   할아버지께서는 조카가 도와드린 것에 대해 감사 인사를 하셨습니다.

6. `act=0.9682` `token='했습니다'`  
   정부는 국경 검문소를 엄격히 관리함으로써 외국인의 불법 입국을 막기 위해 특별한 허가 체계를 도입했습니다.

7. `act=0.9510` `token='했습니다'`  
   교사는 학생들이 보고서를 제출하도록 돕기 위해 추가 조언을 제공했습니다.

8. `act=0.9393` `token='했습니다'`  
   직원들은 자연 보호구역 내에서 동물들의 이동을 허용하도록 관리 방침을 조정했습니다.

## Candidate 2: feature 6025

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.762`
- validation effect: `+0.065`
- test effect: `+0.840`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.623`

### Top natural activations

1. `act=0.6772` `token='▁ek'`  
   Tavanda duran fazla sütü ekmeğimle birlikte marketten aldığım yemyeşil biber ile hazırladığım salataya koydum.

2. `act=0.6592` `token='▁ek'`  
   Bu erkek öğrenci ve kız arkadaşları yemek olarak ekmek almayı tercih etti.

3. `act=0.6386` `token='限'`  
   飛行機の機内では隣の座席のおじさんがずっと眠りにつき、窓の外には無限に広がる雲海を見ながら、静かな時間が流れていくことに誰も文句を言わない。

4. `act=0.6348` `token='▁ek'`  
   Misafirler için konukseverlik kurallarına uyarak hem sıcak bir çorba hem de taze ekmek verdik.

5. `act=0.6339` `token='했습니다'`  
   실험실에서 그들은 화학 반응을 촉진하도록 특별한 촉매를 사용했습니다.

6. `act=0.6329` `token='▁ek'`  
   Toplantıda herhangi bir yazılı bildiri yayımlanmazken, sözlü açıklama yapan bakan programa yapılacak ek bütçe tahsisi konusunda net bir duruş sergilemedi.

7. `act=0.6325` `token='▁ek'`  
   Yemeğin tadını tam hissedebilmek için biraz tuz eklemek gerekmiyor ama genellikle yapılır.

8. `act=0.6281` `token='▁ek'`  
   Yakın tarihli iklim araştırmalarına göre, kutupların ısınma oranı ekvatora oranla iki kat daha hızlı oluyor.

## Candidate 3: feature 2373

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.877`
- validation effect: `+0.875`
- test effect: `+0.233`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.661`

### Top natural activations

1. `act=1.0129` `token='yor'`  
   Galatasaray'ın bu sezon ligi kazanacağını düşünüyoruz, çünkü son dört maçta mağlubiyetsiz kalmaları ve rakiplerinin zayıf bir dönem geçirmesiyle ilgili bu durum, onların şampiyonluk yolunda olacaklarına dair güçlü bir gösterge niteliği taşıyor.

2. `act=0.9924` `token='ıyor'`  
   Ofisimizdeki düzenli toplantıların her geçen gün daha üretken hâle gelmesi, çalışanların problemleri birlikte çözmek ve yeni fikirler ortaya koymak için doğrudan görüşmeler yapmalarından kaynaklanıyor.

3. `act=0.9839` `token='yor'`  
   Halk refahı adına yapılan çalışmalar arasında kültürel mirasın korunması ve geleneksel sanatların modern dünyaya aktarılması da önemli bir yer tutuyor.

4. `act=0.9701` `token='yor'`  
   İş yerinde bir toplantı yapılacağı için genel müdürün direktifleri doğrultusunda hazırlıklar hızla sürüyor.

5. `act=0.9576` `token='ıyor'`  
   Bu durumun nedeni büyük ihtimalle geçen hafta yapılan bakım çalışmasından kaynaklanıyor olabilir, çünkü o günden beri makine biraz daha sessiz ve düzgün çalışıyor gibi görünüyor.

6. `act=0.9548` `token='yor'`  
   Aile toplantısında herkesin kendi fikrini açıkça ifade etmesi ve diğer katılımcıların bu fikirlerine saygılı yaklaşması büyük önem taşıyor.

7. `act=0.9522` `token='ıyor'`  
   Bilimsel araştırmalar yaparken veri analizi sonuçlarının yorumlanması bana her zaman yeni perspektifler kazandırıyor.

8. `act=0.9499` `token='uyor'`  
   Yeni araştırma, bilim insanlarının önceki çalışmalara göre karbon emisyonlarının azaltılmasının çok daha dikkatli ve kararlı şekilde yürütülmeye başlanması gerektiğini söylediğini ortaya koyuyor.

## Candidate 4: feature 9261

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.862`
- validation effect: `+0.606`
- test effect: `+0.502`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.542`

### Top natural activations

1. `act=1.3896` `token='습니다'`  
   정부는 아동들의 건강한 식습관을 형성하기 위해 학교 급식 메뉴에서 인스턴트 식품의 제공을 제한하도록 지자체에 지침을 내렸습니다.

2. `act=1.3648` `token='습니다'`  
   정치 선언이 예상보다 훨씬 더 극단적이었다니 놀랍습니다.

3. `act=1.3624` `token='습니다'`  
   반면 교육 투자율은 높아졌습니다.

4. `act=1.3509` `token='습니다'`  
   이번 실험에서 동생이 전혀 예상하지 못한 유전적 관계를 밝혀내어 모두가 놀랐습니다.

5. `act=1.3435` `token='습니다'`  
   놀랍게도, 프로젝트 일정이 어제 갑작스럽게 변경되어 전체 팀이 혼란에 빠졌습니다.

6. `act=1.3430` `token='습니다'`  
   할아버지께서는 조카가 도와드린 것에 대해 감사 인사를 하셨습니다.

7. `act=1.3346` `token='습니다'`  
   회의실에서 발표 준비를 마친 후, 점심을 같이 먹자는 제안이 나왔습니다.

8. `act=1.3271` `token='습니다'`  
   경기 결과는 정말 놀랍게 나왔습니다.

## Candidate 5: feature 3341

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.824`
- validation effect: `+0.741`
- test effect: `+0.291`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.511`

### Top natural activations

1. `act=1.0876` `token='ことができます'`  
   この先の観光地では、多くの観光客が自然を敬って歩く様子が見られ、地元の方が丁寧に案内してくれるので、ゆっくりと美しい風景を味わうことができます。

2. `act=1.0746` `token='います'`  
   新しいことに挑戦するには、自分にとって最適な学び方を見つけるのが大切で、例えば、資料を読むよりも講義の動画を見る方がよく理解できるという人もいます。

3. `act=1.0593` `token='ります'`  
   定期的に健康診断を受けることは、早期に病気の兆候を見逃さず適切な治療を開始するための大切なステップであり、医師からも生活習慣や栄養バランスについてアドバイスをもらう機会にもなります。

4. `act=1.0512` `token='ります'`  
   旅行先でのアクティビティの予定を共有する際には、目的地が明確であれば相手に自分の名前を言わなくても伝わります。

5. `act=1.0396` `token='います'`  
   図書館では静かに座って勉強する人もいれば、大声で話し合いながらのグループワークをする人もいます。

6. `act=1.0194` `token='ことがあります'`  
   しかし、特に量子力学のような科学分野では、ある現象の観測がシステムに与える影響を理解するためには、まず観測対象そのものの性質と、それを測定しようとする装置や方法の制約に注目することが重要であり、これにより理論的な予測と実験結果のずれを説明する糸口が得られることがあります。

7. `act=0.9880` `token='と思います'`  
   お出かけの際に、ご予定の電車時刻を確認しておくと、スムーズに移動できると思います。

8. `act=0.9719` `token='からです'`  
   それでは、私のお勧めはあのプロジェクトではなくて、こっちの取り組みに関する一歩を踏み出すことなんですけど、なぜならあれはかなり厳しい予算制限がありながらも実績を残すのは難しいからです。

---

# Variable 38: speech_act_force_and_request_directness

- Original SAE evidence tier: **A**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.907**

## Candidate 1: feature 3396

- selection: `original_trainval_selected`
- train effect: `+0.440`
- validation effect: `+0.057`
- test effect: `+0.400`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.502`

### Top natural activations

1. `act=2.1992` `token='to'`  
   Era da tanto che non mangiavo qualcosa di davvero buono, quindi quando ho sentito il profumo del sugo che bolliva mi sono seduto al tavolo e ho aspettato senza dire niente, certo che lui l’avesse già preparato per tutti.

2. `act=2.1061` `token='u'`  
   Je suis arrivé à l’aéroport hier matin et j’ai attendu longtemps avant que mon vol ne décolle finalement en début d’après-midi.

3. `act=2.0978` `token='re'`  
   Mentre preparavo la cena e lui mi aiutava mettendo a posto gli ingredienti, ci siamo dimenticati di accendere il forno e abbiamo dovuto aspettare un po' prima di poter infornare i biscotti che avevamo appena creato.

4. `act=2.0669` `token='дали'`  
   Пассажиры с нетерпением ждали, пока официант разносил горячий кофе по столикам в зале ожидания аэропорта.

5. `act=2.0183` `token='дала'`  
   Вчера вечером я сидела дома и ждала, когда же он наконец приедет.

6. `act=2.0063` `token='дали'`  
   Пассажиры терпеливо ждали в очереди, держа билеты на руках.

7. `act=1.9428` `token='▁esperar'`  
   Ayer visitamos la casa de mis tíos y tuvimos que esperar mucho.

8. `act=1.9138` `token='re'`  
   L'aereo atterrò con due ore di ritardo e bisognò aspettare l'emissione dei biglietti per continuare il viaggio.

## Candidate 2: feature 5707

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.451`
- validation effect: `+0.715`
- test effect: `+0.437`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `1.126`

### Top natural activations

1. `act=1.6447` `token='▁لم'`  
   قالت المعلمة إنك إذا لم تهتم بمذاكرة فإنك لن تنجح في الامتحان النهائي.

2. `act=1.6300` `token='▁no'`  
   El conductor les advirtió a los pasajeros que, si no reducían la velocidad al cruzar el puente, podrían sufrir un accidente grave debido al viento fuerte y la visibilidad limitada.

3. `act=1.6118` `token='▁no'`  
   El doctor nos explicó con claridad que la presión arterial alta, si no se controla adecuadamente, puede provocar problemas más graves en el corazón y los riñones, pero lamentablemente fue descuidada por la mayoría de los pacientes en la consulta.

4. `act=1.6045` `token='▁hay'`  
   El médico me explicó que el tratamiento se debe administrar con cuidado y que, si hay efectos secundarios graves, debo dejarlo inmediatamente y consultar nuevamente para que me revisen.

5. `act=1.5967` `token='re'`  
   Her mother mentioned that she had told her brother, "If you're going to leave, at least say goodbye."

6. `act=1.5608` `token='re'`  
   We've got a basketball game tomorrow afternoon, so if you're planning on hanging around the gym, maybe clear your schedule first.

7. `act=1.5353` `token='▁no'`  
   El científico observó cómo el río crecía rápidamente y declaró: "Si no se actúa pronto, el desbordamiento será inevitable e inundará las zonas bajas cercanas".

8. `act=1.5314` `token='re'`  
   I suppose that if you're aiming to apply for a scholarship, you might want to check the eligibility criteria first, just so you can make sure your application stands a real chance.

## Candidate 3: feature 13976

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.438`
- validation effect: `+0.239`
- test effect: `-0.138`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `2`
- specificity ratio: `0.874`

### Top natural activations

1. `act=1.9906` `token='▁zaman'`  
   Bir sosyal etkileşim modeli geliştirmek için katılımcıların grup içindeki davranışlarının nasıl değiştiğini analiz eden araştırmacılar, yoğun bir görüşme ortamında bireylerin kimi zaman daha aktif, kimi zaman ise pasif roller aldığını gözlemlemişlerdir.

2. `act=1.8717` `token='valda'`  
   Köylü geldiğinde elinde iki büyük çuval vardı ve bir çuvalda buğday bir çuvalda mısır olduğu görülüyordu.

3. `act=1.7110` `token='有人'`  
   咖啡店裡的陽光灑在木質桌面上，這家開在火車站附近的小店總是人來人往，有人專心地讀書、有人低聲談論旅遊行程，而我則靜靜地看著這一幕，點了一杯拿鐵，享受著短暫的放鬆時刻。

4. `act=1.7089` `token='▁mal'`  
   Je nachdem, wie man das Licht setzt, wirkt ein Gemälde mal fröhlich, mal düster.

5. `act=1.6862` `token='i'`  
   Ofis binasına gelen üç bayan birbirlerine benziyorlardı ama her biri farklı bölümlerden, biri maliyeden, diğeri personel şubesinden ve üçüncüsü de pazarlama ekibinden geliyordu.

6. `act=1.6786` `token='邊'`  
   家裡的蘿蔔燉牛肉香氣四溢，媽媽在廚房裡一邊翻炒青菜一邊叮囑爸爸記得關火，而我則端著剛烤好的紅蘿蔔蛋糕走進客廳，準備搭配這週末特製的手工抹茶紅豆包一起享用。

7. `act=1.6745` `token='▁ne'`  
   'Pazar öncesi hazırlıklarımızda ne ekmek aldık, ne süt, ne de yumurta' dedi Leyla, yemeğin tuzsuz geçtiğini fark ettiğimizde.

8. `act=1.6589` `token='有'`  
   那里有山，这里有海。

## Candidate 4: feature 14406

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.428`
- validation effect: `+0.614`
- test effect: `+0.089`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `3`
- specificity ratio: `0.874`

### Top natural activations

1. `act=1.2669` `token='!'`  
   先生が突然、私たちのクラスで小テストを行うと発表したとき、皆は驚いて「えーっ！？」と声を上げた。

2. `act=1.2639` `token='!'`  
   これが未来の科学だなんて、本当に驚いた！

3. `act=1.2393` `token='!'`  
   Aman ya! Bunu kimse düşünmemiş miydi daha önce?

4. `act=1.2254` `token='!'`  
   えええーっ！忘れ物をしていたなんて、信じられないよ！

5. `act=1.2242` `token='!'`  
   なんて美味しいの、これ！

6. `act=1.2239` `token='!'`  
   なんということだろう、この新しい発見は！

7. `act=1.2092` `token='!'`  
   きさらぎの病気が見つかったなんて、信じられない！

8. `act=1.2091` `token='!'`  
   こんなにも未来を感じさせる科学技術が、この街角に実現されているなんて！

## Candidate 5: feature 2145

- selection: `train_fwer_plus_val_direction`
- train effect: `+0.426`
- validation effect: `+0.091`
- test effect: `-0.035`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.733`

### Top natural activations

1. `act=1.5798` `token='▁которое'`  
   Студенты, которые много времени уделяли подготовке к выставке произведений графики и живописи, в конце концов получили то признание, на которое так надеялись, и это позволило им закрепиться в центре современного искусства.

2. `act=1.5621` `token='▁чего'`  
   Мне посоветовали обратиться к специалисту, потому что если не заботиться о здоровье самому, то даже самые близкие люди начнут беспокоиться и рекомендовать что-то такое, чего ты вовсе не хочешь делать.

3. `act=1.5519` `token='▁che'`  
   Mi è capitato spesso di sentire dire da amici o conoscenti che, pur seguendo una dieta sana e facendo regolare attività fisica, si sentivano stanchi e poco motivati, quasi come se mancasse loro qualcosa che non riuscivano né a identificare né a comunicare bene agli altri.

4. `act=1.5479` `token='▁което'`  
   Седнах на терасата пред кафенето и видях със собствени очи как младият мъж разговаряше с местните жители и се старайки да ги убеди в нещо, което изглеждаше важно за него.

5. `act=1.5442` `token='▁чего'`  
   Мне не нравится, когда меня заставляют делать то, чего я не хочу.

6. `act=1.5171` `token='▁которую'`  
   Всё утро длилась суета из-за того, что в холодильник случайно попала обувь, которую кто-то забыл дома, и запах привлёк курьеров, домработниц, соседей по лестничной клетке и даже представителя юридической фирмы, проверявшего документы на содержание животных в этом подъезде.

7. `act=1.5132` `token='▁che'`  
   Quando torniamo da quella gita fuori città che abbiamo organizzato per ricongiungerci con i cugini di mia madre, trovo sempre un enorme sollievo nel lasciare alle spalle le tensioni quotidiane e sentirmi parte di qualcosa che va oltre me stesso.

8. `act=1.5013` `token='▁которое'`  
   У меня уже давно нет того недомогания, которое однажды настолько ослабило меня, что я несколько дней не мог ни есть, ни пить, но зато теперь я могу гораздо лучше понимать, как важно ухаживать за своим здоровьем.

---

# Variable 39: deixis_and_perspective_anchoring

- Original SAE evidence tier: **B2**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.731**

## Candidate 1: feature 14441

- selection: `original_trainval_selected`
- train effect: `-0.702`
- validation effect: `-0.316`
- test effect: `-0.270`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `1`
- specificity ratio: `2.027`

### Top natural activations

1. `act=1.4452` `token='現在'`  
   彼は母が厳しい教育方針を取っていたことを振り返りながら、それが現在の成功に繋がっていると述べた。

2. `act=1.4441` `token='今'`  
   その講義で彼が述べた当時の教育方針は、今振り返ると時代錯誤だったように思える。

3. `act=1.4194` `token='現在'`  
   この美術作品は、もともとは東京国立近代美術館のコレクションに所属していたにもかかわらず、修復作業が十分に行われず、その後展示機会も限られていたため、現在の保存状態では評価が難しいと専門家は指摘している。

4. `act=1.4170` `token='▁지금'`  
   축구를 처음 시작할 때는 공을 차는 법도 제대로 몰라서 주눅이 들었는데, 지금은 팀에서 맨 시야까지 넓혀서 수비수와의 연결도 잘 되고 있어서 정말 많이 성장한 것 같아요.

5. `act=1.4167` `token='今'`  
   展示会の最後の日に、偶然にもかつての同級生が隣に座っていて、彼女が私が幼くてもっとも熱心に描いていた絵を、今や展覧会で公開していることに、私は驚きと誇りで胸が一杯になった。

6. `act=1.4096` `token='今'`  
   私が東京にいた頃は毎朝通勤電車でストレスを感じていたのに、今は地方ののどかな列車の遅れにも気にならない。

7. `act=1.3830` `token='▁bugün'`  
   Geçmişte babamın bize öğrettikleri anılarını bugünkü görüşlerle ele alırken, çocukluğumuzun o anlarında bir aile olarak yaşanan bilinçsizlikten daha fazla şeyin varlığını anlamaya çalışıyoruz.

8. `act=1.3827` `token='今'`  
   山梨県の見附峠で、観光客が古い地図と現地の地形を比較していたところ、かつて存在していたとされる失われた道が今なお一部残っていることに驚きの声を上げていた。

## Candidate 2: feature 9622

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.763`
- validation effect: `-0.472`
- test effect: `-0.527`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `7`
- specificity ratio: `0.883`

### Top natural activations

1. `act=1.3681` `token='.'`  
   I just uploaded my highlight reel from the summer league to /Videos/2023_Basketball_Camp_Highlights.mp4.

2. `act=1.3502` `token='.'`  
   Je viens de télécharger un rapport intitulé "Étude_du_jeune_Antoine_14_ans_Mars2025.pdf" qui détaille son suivi médical depuis la vaccination.

3. `act=1.3009` `token='.'`  
   Müzik koleksiyonumda en çok sevdiğim albümün dosya adı "04_Güz_Ağustos_Tatili.mp3" olarak kayıtlı.

4. `act=1.2960` `token='.'`  
   Я приглашаю вас на день рождения моей сестры.

5. `act=1.2753` `token='。'`  
   ご案内ありがとうございます。空港までお送りいたします。

6. `act=1.2705` `token='.'`  
   Ich melde mich morgen bei euch.

7. `act=1.2603` `token='。'`  
   山田さん、明日のミーティングにはどうぞお越しください。

8. `act=1.2479` `token='.'`  
   Yağmurlu pazar sabahı, annem bana gönderdiği "2024_cumartesi_pazartesi_yolculugu_planlari.xlsx" dosyasını açtığımda annemle babamın bekledikleri gibi planlarla ilgili tartışmalarımız oldukça uzun sürdü.

## Candidate 3: feature 11602

- selection: `train_fwer_only`
- train effect: `-0.625`
- validation effect: `+0.000`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.765`

### Top natural activations

1. `act=1.3420` `token='▁hier'`  
   Il me l’a prescrit hier, mais je ne l’ai pas encore acheté.

2. `act=1.3420` `token='▁hier'`  
   Il me l’a prescrit hier, mais je ne me sens toujours pas mieux.

3. `act=1.3211` `token='▁hier'`  
   Wenn er angerufen hätte, würden wir heute hier sein.

4. `act=1.3095` `token='▁hier'`  
   Il a terminé son tableau hier soir.

5. `act=1.3079` `token='▁hier'`  
   Wenn du gewollt hättest, würdest du hier sein.

6. `act=1.3057` `token='▁hier'`  
   Hätte sie angerufen, würde ich jetzt nicht hier sitzen.

7. `act=1.3030` `token='▁hier'`  
   Ich glaube, die nächste U-Bahn wird in etwa fünf Minuten hier sein.

8. `act=1.2873` `token='▁hier'`  
   Könntest du kurz die Lampe etwas dimmen, damit es hier nicht so hell ist?

## Candidate 4: feature 6132

- selection: `train_fwer_only`
- train effect: `-0.623`
- validation effect: `+0.000`
- test effect: `-0.256`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `True`
- full survival: `False`
- specificity rank among 40: `1`
- specificity ratio: `1.498`

### Top natural activations

1. `act=1.6773` `token='పు'`  
   నేను, నా సోదరుడు మరియు మా అమ్మ రేపు నగరంలోకి వెళ్తాం.

2. `act=1.6281` `token='n'`  
   Küçük kardeşim yarın burada olacak, hepsini birlikte çözelim diyor.

3. `act=1.5960` `token='పు'`  
   మనం రేపు అక్కడకు వెళ్లాలి, నీకు కావలసిన ఏదైనా చెప్పు.

4. `act=1.5960` `token='పు'`  
   మనం రేపు సినిమాకు వెళ్ళడానికి అలవాటు.

5. `act=1.5946` `token='n'`  
   Kız kardeşim yarın konuk olarak bizimle kahvaltı yapacakmış.

6. `act=1.5946` `token='n'`  
   Kız kardeşim yarın sabah ders çalışmaya gidecek.

7. `act=1.5377` `token='n'`  
   Ahmet'in, yarın buluşmamız olduğunu söylediğini duydum.

8. `act=1.5335` `token='n'`  
   Kardeşim yarın bizimle gelecekmiş.

## Candidate 5: feature 4923

- selection: `train_fwer_only`
- train effect: `+0.689`
- validation effect: `-0.409`
- test effect: `+0.406`
- train maxT significant: `True`
- validation same direction: `False`
- test same direction: `True`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.825`

### Top natural activations

1. `act=1.2777` `token='.'`  
   Had we trained harder, we'd have won the championship.

2. `act=1.2431` `token='.'`  
   Si te hubieras casado conmigo, ahora seríamos abuelos.

3. `act=1.2251` `token='.'`  
   If we had trained harder, we might have won the championship.

4. `act=1.2057` `token='。'`  
   这个数据是今天的，那个是昨天的。

5. `act=1.2029` `token='.'`  
   Si tu avais travaillé plus, tu aurais réussi l'examen.

6. `act=1.1954` `token='.'`  
   Wenn ich damals mehr gearbeitet hätte, wäre ich heute nicht hier.

7. `act=1.1882` `token='.'`  
   Had he trained harder, he'd have made the team.

8. `act=1.1828` `token='.'`  
   Wenn wir damals doch nur den Zug genommen hätten, statt das beschädigte Auto mitzunehmen, wären wir jetzt schon in Andalusien, statt hier im Stau zu stehen und uns zu fragen, ob wir je ankommen werden.

---

# Variable 40: orthographic_and_tokenization_interface

- Original SAE evidence tier: **D**
- Probe core status: **no_core_pass_0of3**
- Layer-12 mean delta probe test AUROC: **0.499**

## Candidate 1: feature 3132

- selection: `original_trainval_selected`
- train effect: `-0.418`
- validation effect: `-0.141`
- test effect: `+0.246`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `3`
- specificity ratio: `0.836`

### Top natural activations

1. `act=0.9802` `token=','`  
   The new policy, which was announced during a press conference yesterday by the minister of finance, aims to increase transparency in government spending and hold officials accountable for budget overruns.

2. `act=0.9694` `token=','`  
   El informe, además de ser presentado en la reunión, fue revisado cuidadosamente por el equipo de investigación antes de su envío oficial al comité académico.

3. `act=0.9649` `token=','`  
   La mostra, pur essendo molto apprezzata dal pubblico e dagli esperti del settore, non è riuscita a raggiungere l’obiettivo delle entrate previste per coprire i costi di allestimento.

4. `act=0.9579` `token=','`  
   It was announced yesterday that the new policy, aimed at improving transparency within government operations, will be implemented across all departments starting next month.

5. `act=0.9360` `token=','`  
   Les chercheurs ont observé que la nouvelle molécule, extraite d'une algue peu étudiée jusqu'à présent, pourrait être utilisée pour améliorer les traitements anticancéreux existants.

6. `act=0.9313` `token=','`  
   La obra, que se presentó el año pasado, fue un éxito rotundo y marcó un antes y después en la carrera del artista.

7. `act=0.9313` `token=','`  
   La obra, que fue presentada el jueves pasado y se mostró nuevamente ayer, sigue recibiendo críticas elogiosas de la prensa especializada.

8. `act=0.9299` `token=','`  
   The mayor, who was speaking at the town hall meeting, emphasized that the new policy, which had been approved by the council with bipartisan support, would take effect on Monday.

## Candidate 2: feature 16180

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.431`
- validation effect: `-0.386`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `4`
- specificity ratio: `0.623`

### Top natural activations

1. `act=1.4083` `token=','`  
   Il est évident que la récente reconstitution des fresques de l’église Santa Maria delle Grazie repose sur une méthode de datation par thermoluminescence qui permet d’identifier avec certitude la période exacte de leur exécution, confirmant ainsi la précision des archives historiques et les compétences techniques des restaurateurs italiens.

2. `act=1.3986` `token=','`  
   Cuando revisamos los registros del sistema de control interno, nos sorprendimos al descubrir que la auditoría automatizada había omitido más del diez por ciento de las transacciones sospechosas, lo cual plantea un riesgo significativo para la integridad de nuestros procesos financieros.

3. `act=1.3905` `token=','`  
   La teoría de la relatividad que mi profesor mostró en clase nos ayudó a comprender mejor cómo el tiempo y el espacio están intrínsecamente relacionados, y qué compleja resulta la idea de que dos personas puedan experimentar lo mismo de forma diferente según su movimiento relativo.

4. `act=1.3787` `token=','`  
   El equipo de fútbol que entrena en la cancha principal desde las cinco de la tarde ha demostrado un progreso notable en el manejo del balón, la coordinación entre los jugadores y el dominio táctico durante los últimos tres meses.

5. `act=1.3769` `token=','`  
   L'art contemporain continue de refléter une tendance marquée vers l'abstraction et l'expression libre des émotions, souvent en s'éloignant des normes traditionnelles pour explorer de nouvelles formes d'interprétation visuelle et conceptuelle.

6. `act=1.3718` `token=','`  
   En la nueva reforma educativa se destacó el esfuerzo por fomentar una mayor autonomía de los docentes en la elaboración de las estrategias pedagógicas, lo cual reflejaba una clara apuesta por un modelo más participativo y dinámico en la enseñanza.

7. `act=1.3711` `token=','`  
   Como resultado de las protestas masivas en el centro del país, el gobierno anunció ayer un paquete de reformas económicas diseñadas para reducir la desigualdad y estabilizar la inflación, medida que según los expertos podría sentar las bases para una reactivación sostenible del sector productivo.

8. `act=1.3640` `token=','`  
   Selon un récent sondage réalisé par l’institut OpinionWay, la majorité des Français expriment leur préférence pour des lois plus strictes concernant la protection de l’environnement, tout en souhaitant que ces mesures ne pénalisent pas excessivement les petites entreprises.

## Candidate 3: feature 9673

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.455`
- validation effect: `-0.198`
- test effect: `-0.126`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `5`
- specificity ratio: `0.747`

### Top natural activations

1. `act=1.5025` `token='▁ya'`  
   Aunque mis hermanas y yo siempre tuvimos gustos muy distintos, incluso en cosas simples como la música o los colores que nos agradaban, eso nunca afectó nuestra relación, ya que supimos valorar esas diferencias como algo que enriquecía más lo que compartíamos.

2. `act=1.4957` `token='▁bai'`  
   Gizarte-problema horiek aurrera egin behar direla uste dut, baina hautagaien argudioak ez dira behin-behineko akatsak izatea ahalduko diguten, baizik eta bereizi dezakeguelarik tresna honetan dauden babes-erroren neurketa egiten dutelarik.

3. `act=1.4784` `token='▁ya'`  
   Cuando viajo en tren por el sur de España, siempre me sorprende lo distintos que nos comportamos las personas según el lugar y la hora, ya sea saliendo tarde en verano o atravesando paisajes fríos en invierno.

4. `act=1.4769` `token='▁ya'`  
   Cuando uno piensa en los tíos que tienen más de dos hijos en la familia, siempre terminan ayudando con algo, ya sea con el jardín o con las tareas escolares de los sobrinos más pequeños.

5. `act=1.4678` `token='▁ya'`  
   Es imposible que ningún jugador haya cometido errores ni hayan fracasado en lograr los objetivos establecidos durante la temporada anterior, ya que todos estuvieron ausentes de cualquier actitud negativa o conducta indisciplinada.

6. `act=1.4644` `token='▁ya'`  
   Es evidente que el profesor se había preparado concienzudamente para la clase sobre los clásicos literarios, ya que sus explicaciones eran profundas, claras y reflejaban una gran familiaridad con los textos.

7. `act=1.4638` `token='▁ya'`  
   Esperaba que por la noche todo el mundo se sentara tranquilamente en la sala de estar y disfrutara del concierto en televisión, ya que habíamos invitado a algunos amigos de la Universidad.

8. `act=1.4609` `token='▁ب'`  
   رُبَّمَا نَجِدُ فِي الصُّحُفِ تَقْلِيدًا لِلتَّفَاعُلَاتِ الْأُمَّيَّةِ، بَلْ يَكُونُ هَذَا أَمْرًا مُؤَثِّرًا فِيمَا يَقُومُ بِهِ النَّاسُ فِي مُجَالِ الْعَمَلِ الْجَمَ

## Candidate 4: feature 2602

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.472`
- validation effect: `-0.399`
- test effect: `+0.000`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `False`
- full survival: `False`
- specificity rank among 40: `6`
- specificity ratio: `0.748`

### Top natural activations

1. `act=1.7972` `token=','`  
   Според репортажа от мача, тимът на футболистите победи с убедителен резултат след продължително и висококласно съперничество между двата отбора.

2. `act=1.7692` `token=','`  
   Пейсът постепенно навлиза в детайли и емоциите му се променят от момента, в който започва до този, в който завършва.

3. `act=1.7420` `token=','`  
   Sie meinte, dass es im Team immer wieder Diskussionen gäbe, doch als ich nachfragte, erwiderte sie mit einem Lächeln: ‚Es ist nicht immer das, was man hört, sondern das, was man versteht.’

4. `act=1.7373` `token=','`  
   Исследователи не только не смогли подтвердить теорию, но и не нашли ни одного доказательства, подкрепляющего их гипотезу, что серьёзно пошатнуло уверенность в правильности выбранного направления исследований.

5. `act=1.7347` `token=','`  
   ¿Puedo ayudarte con el informe, jefe?

6. `act=1.7335` `token=','`  
   Вчера видях със собствените си очи как новият мениджър на отдела за проекти започна да прави голям шум около начините, по които е възможно да се оптимизира разпределянето на задачите между служителите.

7. `act=1.7249` `token=','`  
   Эти данные не подтверждают теорию, а также не опровергают её полностью.

8. `act=1.7126` `token=','`  
   Видях сестра ми как проверява писъмчето, което са намерили в ателието, и разбрах от начина, по който го свитка, че е било написано точно от него.

## Candidate 5: feature 12291

- selection: `train_fwer_plus_val_direction`
- train effect: `-0.487`
- validation effect: `-0.204`
- test effect: `-0.024`
- train maxT significant: `True`
- validation same direction: `True`
- test same direction: `True`
- full survival: `True`
- specificity rank among 40: `6`
- specificity ratio: `0.646`

### Top natural activations

1. `act=1.3871` `token='▁отец'`  
   Тётя Натальи Петровны, жена брата её сводной сестры, часто рассказывала нам внуким длинные и трогательные истории о далёком детстве, когда дедушка, отец её мужа, ещё не был старым и гулял с детьми по берегам родного села.

2. `act=1.3803` `token='ungen'`  
   Die Suppe kocht von alleine über dem sanften Flämmchen, während die Zwiebeln, gezwungen, sich selbst zu erweichen, langsam ihr Aroma entfalten, und die Gewürze, in Öl eingebraten, ihre Kraft geben, ohne dass jemand sie direkt bedient.

3. `act=1.3647` `token='po'`  
   ¡Cómo has crecido, guapo!

4. `act=1.3610` `token='tuak'`  
   Zientzia eta teknologia aretoko zaborra gainditzen denean, argazki, datuak, lanaren dokumentazioa eta beste informazio batzuk automatikoki eduki bidez konpartitu eta kudeatu behar dira beste elkarrekin lan egiten dutenekin.

5. `act=1.3584` `token='▁wind'`  
   The river, winding through the valley that lies between those tall mountains you can see from the road, was swollen with spring melt and rain from the previous week’s storm, which had turned the usually dry stream beds along its banks into temporary tributaries flowing with mud and debris.

6. `act=1.3531` `token='▁quiet'`  
   This time of year, the office, quiet as a library, hums with deadlines.

7. `act=1.3239` `token='▁konuk'`  
   Ev sahibi, konukları için lezzetli bir yemek hazırlamayı unutmadı.

8. `act=1.3054` `token='▁baba'`  
   Annemin kocası babam, babamın kızı benseyim, ama kardeşim olan abimin oğlu da benim yeğenimdir, herkes birbirine nasıl bağlı olduğunu çok net bilir çünkü annem, babam, ben ve ailemiz hep evde oturduk.

---

