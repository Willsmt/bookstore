import pytest
from product.models import Category
from product.tests.factories import ProductFactory


@pytest.mark.django_db
class TestProduct:
    def test_product_nasce_ativo_por_padrao(self):
        product = ProductFactory()
        assert product.is_active is True

    def test_preco_negativo_nao_e_bloqueado_so_pelo_save(self):
        # Pegadinha real: MinValueValidator no campo NAO roda em .save()/.create()
        # direto — só via full_clean() (forms/admin) ou pela validacao do DRF.
        # Isso e esperado, nao e bug: quem cria Product sempre passa pelo
        # ProductSerializer, entao a validacao acontece na API mesmo assim.
        product = ProductFactory.build(price=-10)
        product.save()
        assert product.price == -10  # confirma a lacuna, documentada


@pytest.mark.django_db
class TestCategory:
    def test_slug_gerado_automaticamente_quando_nao_informado(self):
        category = Category(name="Ficção Científica")
        category.save()
        assert category.slug == "ficcao-cientifica"

    def test_slug_customizado_e_respeitado(self):
        category = Category(name="Ficção", slug="meu-slug")
        category.save()
        assert category.slug == "meu-slug"
