import os
import shutil
import unittest
from app import sync_folders


class TestFolderSync(unittest.TestCase):
    source_folder = "C:\\Users\\nuno_\\Documents\\GitHub\\The-Synchronizer\\unittest\\teste"
    replica_folder = "C:\\Users\\nuno_\\Documents\\GitHub\\The-Synchronizer\\unittest\\teste2"
    log_file = "C:\\Users\\nuno_\\Documents\\GitHub\\The-Synchronizer\\unittest\\log.txt"

    @classmethod
    def setUpClass(cls):
        # Limpar o log de teste antes de cada execução
        open(cls.log_file, 'w').close()

    def setUp(self):
        # Criar as pastas de teste antes de cada teste
        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.replica_folder, exist_ok=True)

    def tearDown(self):
        # Remover as pastas de teste e o arquivo de log após cada teste
        shutil.rmtree(self.source_folder)
        shutil.rmtree(self.replica_folder)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_copy_files(self):
        # Teste de cópia inicial de arquivos da origem para a réplica
        open(os.path.join(self.source_folder, 'file1.txt'), 'w').write("Content 1")
        open(os.path.join(self.source_folder, 'file2.txt'), 'w').write("Content 2")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se os arquivos foram copiados corretamente
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, 'file2.txt')))

    def test_update_file(self):
        # Teste de atualização de arquivo já existente na réplica
        open(os.path.join(self.source_folder, 'file1.txt'), 'w').write("New Content")
        open(os.path.join(self.replica_folder, 'file1.txt'), 'w').write("Old Content")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se o arquivo foi atualizado
        with open(os.path.join(self.replica_folder, 'file1.txt'), 'r') as f:
            content = f.read()
        self.assertEqual(content, "New Content")

    def test_delete_file(self):
        # Teste de exclusão de arquivo da réplica quando removido na origem
        open(os.path.join(self.source_folder, 'file1.txt'), 'w').write("Content")
        open(os.path.join(self.replica_folder, 'file1.txt'), 'w').write("Content")
        open(os.path.join(self.replica_folder, 'file2.txt'), 'w').write("Extra Content")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se o arquivo extra foi deletado da réplica
        self.assertFalse(os.path.exists(os.path.join(self.replica_folder, 'file2.txt')))

    def test_create_directory(self):
        # Teste de criação de diretório na réplica quando adicionado na origem
        os.makedirs(os.path.join(self.source_folder, 'subdir'))
        open(os.path.join(self.source_folder, 'subdir', 'file3.txt'), 'w').write("Subdirectory Content")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se o diretório e o arquivo foram copiados
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, 'subdir')))
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, 'subdir', 'file3.txt')))

    def test_delete_directory(self):
        # Teste de exclusão de diretório na réplica quando removido na origem
        os.makedirs(os.path.join(self.source_folder, 'subdir'))
        os.makedirs(os.path.join(self.replica_folder, 'subdir'))
        open(os.path.join(self.replica_folder, 'subdir', 'file4.txt'), 'w').write("Content to be deleted")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se o diretório extra foi deletado da réplica
        self.assertFalse(os.path.exists(os.path.join(self.replica_folder, 'subdir', 'file4.txt')))


    def test_large_file_sync(self):
        large_file_path = os.path.join(self.source_folder, 'large_file.txt')
        with open(large_file_path, 'wb') as f:
            f.write(b'0' * 1024 * 1024 * 100)  # 100 MB file

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se o arquivo grande foi copiado
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, 'large_file.txt')))

    def test_hidden_files_and_directories(self):
        os.makedirs(os.path.join(self.source_folder, '.hidden_dir'))
        open(os.path.join(self.source_folder, '.hidden_file.txt'), 'w').write("Hidden content")

        sync_folders(self.source_folder, self.replica_folder)

        # Verificar se arquivos e diretórios ocultos foram copiados
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, '.hidden_dir')))
        self.assertTrue(os.path.exists(os.path.join(self.replica_folder, '.hidden_file.txt')))


if __name__ == '__main__':
    unittest.main()
