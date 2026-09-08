from django.db import migrations

ANOS = [
    {
        'numero': 1,
        'descricao': (
            'Fundamentos da programação, lógica, introdução à computação e '
            'primeiros passos no desenvolvimento web.'
        ),
    },
    {
        'numero': 2,
        'descricao': (
            'Banco de dados, engenharia de software, desenvolvimento web '
            'avançado e projetos integrados.'
        ),
    },
    {
        'numero': 3,
        'descricao': (
            'Desenvolvimento web avançado, mobile, redes de computadores e '
            'projeto final integrador.'
        ),
    },
]

DISCIPLINAS = {
    1: [
        {
            'slug': 'logica',
            'nome': 'Lógica de Programação',
            'icone': 'mdi-language-javascript',
            'descricao': (
                'Desenvolvimento do raciocínio lógico, algoritmos e fundamentos '
                'da programação.'
            ),
        },
        {
            'slug': 'web1',
            'nome': 'Desenvolvimento Web I',
            'icone': 'mdi-vuejs',
            'descricao': (
                'Estruturação de páginas web com HTML, CSS e introdução ao JavaScript.'
            ),
        },
        {
            'slug': 'intro',
            'nome': 'Introdução à Computação',
            'icone': 'mdi-laptop',
            'descricao': (
                'Conceitos fundamentais de computação, hardware, software e '
                'sistemas operacionais.'
            ),
        },
        {
            'slug': 'projeto1',
            'nome': 'Projeto Integrador I',
            'icone': 'mdi-folder-star-outline',
            'descricao': 'Primeiro projeto integrador aplicando os conhecimentos do primeiro ano.',
        },
    ],
    2: [
        {
            'slug': 'banco',
            'nome': 'Banco de Dados',
            'icone': 'mdi-database',
            'descricao': (
                'Modelagem de dados, consultas SQL, normalização e gestão de '
                'bancos de dados relacionais.'
            ),
        },
        {
            'slug': 'software',
            'nome': 'Projeto de Software',
            'icone': 'mdi-cog-outline',
            'descricao': (
                'Metodologias de desenvolvimento de software, UML, requisitos e '
                'gestão de projetos.'
            ),
        },
        {
            'slug': 'web2',
            'nome': 'Desenvolvimento Web II',
            'icone': 'mdi-vuejs',
            'descricao': (
                'Desenvolvimento back-end e front-end com foco em aplicações web completas.'
            ),
        },
        {
            'slug': 'projeto2',
            'nome': 'Projeto Integrador II',
            'icone': 'mdi-folder-star-outline',
            'descricao': (
                'Projeto integrador combinando banco de dados, web e engenharia de software.'
            ),
        },
    ],
    3: [
        {
            'slug': 'web3',
            'nome': 'Desenvolvimento Web III',
            'icone': 'mdi-language-python',
            'descricao': (
                'Frameworks modernos, APIs, autenticação e arquiteturas avançadas de web apps.'
            ),
        },
        {
            'slug': 'mobile',
            'nome': 'Desenvolvimento Web Mobile',
            'icone': 'mdi-cellphone',
            'descricao': (
                'Desenvolvimento de aplicações web responsivas e híbridas para '
                'dispositivos móveis.'
            ),
        },
        {
            'slug': 'projeto3',
            'nome': 'Projeto Integrador',
            'icone': 'mdi-folder-star-outline',
            'descricao': 'Projeto final integrador aplicando todas as competências do curso.',
        },
        {
            'slug': 'redes',
            'nome': 'Redes de Computadores',
            'icone': 'mdi-network',
            'descricao': (
                'Fundamentos de redes, protocolos TCP/IP, configuração de roteadores '
                'e segurança de rede.'
            ),
        },
    ],
}


def seed_catalog(apps, schema_editor):
    Ano = apps.get_model('core', 'Ano')
    Disciplina = apps.get_model('core', 'Disciplina')

    for ano_data in ANOS:
        ano, _ = Ano.objects.get_or_create(numero=ano_data['numero'], defaults=ano_data)
        for disc_data in DISCIPLINAS.get(ano_data['numero'], []):
            Disciplina.objects.get_or_create(
                slug=disc_data['slug'],
                defaults={**disc_data, 'ano': ano},
            )


def unseed_catalog(apps, schema_editor):
    Ano = apps.get_model('core', 'Ano')
    Disciplina = apps.get_model('core', 'Disciplina')

    Disciplina.objects.filter(
        slug__in=[d['slug'] for disc in DISCIPLINAS.values() for d in disc]
    ).delete()
    Ano.objects.filter(numero__in=[a['numero'] for a in ANOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_ano_atividade_arquivo_bloco_disciplina_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, unseed_catalog),
    ]
